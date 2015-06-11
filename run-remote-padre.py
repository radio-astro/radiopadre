#!/usr/bin/python

import os.path
import os
import subprocess
import sys
import select
import time
import re
import socket
import fnmatch

def find_unused_port (base,maxtries=1000):
    for i in range(maxtries):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            serversocket.bind(("localhost", base))
            serversocket.close()
            return base
        except:
            base += 1
            continue
    return None

default_browser = os.environ.get("PADRE_BROWSER","xdg-open")

from optparse import OptionParser,OptionGroup
parser = OptionParser(usage="""%prog: [options] [user@]host[:directory[/notebook.ipynb]]""",
    description="Uses ssh to connect to remote host, runs radiopadre notebook server "+
    "in the specified directory, loads the specified notebook(s) or a default notebook, if any. " +
    "Note that 'notebook' above may contain wildcards."
)

# parser.add_option("--port-query",type=int,metavar="N",
#                   help="looks for N unused ports and reports them. For internal use.");
parser.add_option("-p","--remote-path",type="str",
                  help="directory in which remote run-radiopadre.sh resides. Default is to try ~/radiopadre first, "+
                  "and PATH second.")
parser.add_option("-b","--browser",type="string",default=default_browser,
                  help="browser command to run. Default is %default, or set PADRE_BROWSER.")
parser.add_option("-n","--no-browser",action="store_true",
                  help="do not open a browser for the notebooks.")
parser.add_option("-a","--auto",metavar="PATTERN",type="string",default="default-padre-view.ipynb",
                  help="Auto-open notebook(s) if they exist on remote, "+
                  "and if a notebook is not explicitly specified on the command line. " +
                  "Can be a wildcard pattern. Default is %default. Use -a none to disable auto-open.")

(options,args) = parser.parse_args()

# parse arguments
if len(args) != 1:
    parser.error("incorrect number of arguments")

# parse path to notebook, if notebook even specified
host = args[0]
path = None
notebook = options.auto
if ':' in host:
    host, path = host.split(":",1)
    if path.endswith(".ipynb"):
        notebook = os.path.basename(path)
        path = os.path.dirname(path) 

if options.remote_path:
    padre_execs = [ os.path.join(options.remote_path,"run-radiopadre.sh") ]
else:
    padre_execs = [ "~/radiopadre/run-radiopadre.sh" , "run-radiopadre.sh" ]
# convert to shell OR-statement to try the paths in order
padre_exec = " || ".join(padre_execs)

print "Running remote radiopadre %s, path %s, notebook(s) %s" % (host, path, notebook)

# start ssh subprocess to launch notebook
args = [ "ssh","-tt",host ]
if path:
    args += [ "cd %s && ( %s )" % (path, padre_exec) ]
else:
    args += [ padre_exec ]

ssh = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# poll stdout/stderr
poller = select.poll()
fdlabels = {}

def register_process (po,label=""):
    poller.register(po.stdout)
    poller.register(po.stderr)
    fdlabels[po.stdout.fileno()] = 'stdout'+label, po.stdout
    fdlabels[po.stderr.fileno()] = 'stderr'+label, po.stderr

register_process(ssh,"")

ssh2 = None
auto_notebooks = []

while True:
    try:
        fdlist = poller.poll()
        for fd,event in fdlist:
            line = None
            if event & (select.POLLHUP|select.POLLERR):
                print "ssh process gone, exiting"
                sys.exit(0)
            # which fd is ready? read line and print it
            label,fobj = fdlabels.get(fd)
            line = fobj.readline()
            print "ssh %s: %s" % (label,line.strip())
            # if still looking for available notebooks line, check for it
            if not ssh2:
                # check for available notebooks
                match = line and re.match(".*Available notebooks: (.*)$",line)
                if match:
                    auto_notebooks = [ nb[2:] if nb.startswith("./") else nb 
                                       for nb in match.group(1).strip().split() ]
                    auto_notebooks = fnmatch.filter(auto_notebooks, notebook)
                # check for notebook port, and launch second ssh when we have it
                match = line and re.match(".*Notebook is running at: http://localhost:([0-9]+)/.*",line)
                if match:
                    remoteport = match.group(1);
                    # find unused local port
                    localport = find_unused_port(10000+os.getuid())
                    print "Detected remote port %s, using local port %s" % (remoteport, localport)
                    # start second ssh process to forward the port
                    ssh2 = subprocess.Popen(["ssh","-tt","-L",
                                "%s:localhost:%s" % (localport, remoteport),
                                host,"cat >/dev/null"],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    register_process(ssh2)
                    # open browser if needed
                    path = "http://localhost:%s" % localport
                    if not options.no_browser:
                        print "Opening browser for",path
                        subprocess.Popen([options.browser, path])
                    else:
                        print "-n/--no-browser given, not opening a browser for you"
                        print "Please surf to",path
                    for nb in auto_notebooks:
                        path = "http://localhost:%s/notebooks/%s" % (localport, nb)
                        if not options.no_browser:
                            print "Opening browser for",path
                            subprocess.Popen([options.browser, path])
                        else:
                            print "Please surf to",path
    except KeyboardInterrupt:
        print "Ctrl+C caught"
        ssh.kill()
        ssh2 and ssh2.kill()