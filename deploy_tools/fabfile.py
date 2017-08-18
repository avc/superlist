from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/avc/superlists.git'

def deploy():
    site_folder = f'/home/{env.user}/{env.host}'
    source_folder_name = 'src'
    source_folder = f'{site_folder}/{source_folder_name}'
    virtualenv_folder_name = 'virtualenv'
    project_name = 'superlists'
    
    #_create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host, project_name)
    _update_virtualenv(source_folder, virtualenv_folder_name)
    _update_static_files(source_folder)
    _update_database(source_folder)
    _link_wsgi(site_folder, source_folder_name)
    
def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('db', 'public/static', 'virtualenv', 'src'):
        run(f'mkdir -p {site_folder}/{subfolder}')

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')
    
def _update_settings(source_folder, host, project_name):
    # Debug false
    settings_file = f'{source_folder}/{project_name}/settings.py'
    sed(settings_file, 'DEBUG = True', 'DEBUG = False')
    sed(settings_file, 
        'ALLOWED_HOSTS = .+$', 
        f'ALLOWED_HOSTS = ["{host}"]'
    )

    # Secret key
    secret_key_file = f'{source_folder}/{project_name}/secret_key.py'
    if not exists(secret_key_file):
        chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        secret_key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{secret_key}"')
    append(settings_file, '\nfrom .secret_key import SECRET_KEY')
    
def _update_virtualenv(source_folder, virtualenv_folder_name):
    virtualenv = f'{source_folder}/../{virtualenv_folder_name}'
    if not exists(f'{virtualenv}/bin/pip'):
        run(f'python3 -m venv {virtualenv}')
    run(f'{virtualenv}/bin/pip install -r {source_folder}/requirements.txt')

def _update_static_files(source_folder):
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput'
    )
    
def _update_database(source_folder):
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py migrate --noinput'
    )
    
def _link_wsgi(site_folder, source_folder_name):
    relative_wsgi_file_path = f'{source_folder_name}/deploy_tools/wsgi.py'
    run(
        f'cd {site_folder}'
        f' && ln -sf {relative_wsgi_file_path} passenger_wsgi.py'
    )
