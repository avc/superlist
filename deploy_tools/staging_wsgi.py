import sys, os
VIRTUALENV = "/home/nonzer0/.virtualenvs/django/"
INTERP = VIRTUALENV + "bin/python"
#INTERP is presented twice so that the new Python interpreter knows the actual executable path.
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(cwd + os.sep + 'src')
sys.path.insert(0,cwd+VIRTUALENV+'bin')
sys.path.insert(0,cwd+VIRTUALENV+'lib/python3.6/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = "superlists.settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
