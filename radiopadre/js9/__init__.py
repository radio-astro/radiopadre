import os
import os.path
import traceback
import radiopadre
from radiopadre.render import render_status_message

# init JS9 configuration

# js9 source directory
DIRNAME = os.path.dirname(__file__)

JS9_ERROR = os.environ.get("RADIOPADRE_JS9_ERROR") or None

def init_js9():
    global JS9_ERROR
    if JS9_ERROR:
        return

    global _prefix
    _prefix = radiopadre.SHADOW_URLBASE
    global RADIOPADRE_INSTALL_PREFIX_HTTP
    global RADIOPADRE_LOCAL_PREFIX_HTTP
    global JS9_INSTALL_PREFIX_HTTP
    global JS9_HELPER_PORT
    global JS9_INIT_HTML_HTTP
    global JS9_SCRIPT_PREFIX_HTTP

    RADIOPADRE_INSTALL_PREFIX_HTTP = _prefix + "/radiopadre-www" # URL used to access radiopadre code
    RADIOPADRE_LOCAL_PREFIX_HTTP = os.path.join(_prefix, radiopadre.ABSROOTDIR, ".radiopadre")                     # URL used to access radiopadre aux dir
    JS9_INSTALL_PREFIX_HTTP = _prefix+"/js9-www"  # URL used to access JS9 code
    JS9_SCRIPT_PREFIX_HTTP = _prefix

    try:
        JS9_HELPER_PORT = int(os.environ["RADIOPADRE_JS9_HELPER_PORT"])
    except:
        JS9_ERROR = "invalid RADIOPADRE_JS9_HELPER_PORT setting, integer value expected"


    # get init code, substitute global variables into it
    if not JS9_ERROR:
        try:
            with open(os.path.join(DIRNAME, "js9-init-template.html")) as inp:
                source = inp.read()
            JS9_INIT_HTML_HTTP = source.format(JS9_INSTALL_PREFIX=JS9_INSTALL_PREFIX_HTTP,
                                               RADIOPADRE_INSTALL_PREFIX=RADIOPADRE_INSTALL_PREFIX_HTTP,
                                               RADIOPADRE_LOCAL_PREFIX=RADIOPADRE_LOCAL_PREFIX_HTTP,
                                               **globals())

        except Exception, exc:
            traceback.print_exc()
            JS9_ERROR = "Error reading init templates: {}".format(str(exc))

    # on error, init code replaced by error message
    if JS9_ERROR:
        JS9_INIT_HTML_HTTP = render_status_message("Error initializing JS9: {}".format(JS9_ERROR), bgcolor='yellow')
        radiopadre.add_startup_warning("""Warning: the JS9 FITS viewer is not functional ({}). Live FITS file viewing
            will not be available in this notebook. You probably want to fix this problem (missing libcfitsio-dev and/or nodejs
            packages, typically), then reinstall the radiopadre environment on this system ({}).
            """.format(JS9_ERROR, os.environ['HOSTNAME']))
