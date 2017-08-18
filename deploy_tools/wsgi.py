import sys, os
VIRTUALENV = 'virtualenv'
PROJECT = "superlists"

# The virtualenv directory is a sibling of this file.
virtualenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), VIRTUALENV)
INTERP = virtualenv_path + "/bin/python"
#INTERP is presented twice so that the new Python interpreter knows the actual executable path.
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(cwd + '/src')
sys.path.insert(0, os.path.join(virtualenv_path, 'bin'))
sys.path.insert(0, os.path.join(virtualenv_path, 'lib/python3.6/site-packages'))

os.environ['DJANGO_SETTINGS_MODULE'] = PROJECT + ".settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
