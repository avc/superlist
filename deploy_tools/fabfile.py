from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/avc/superlists.git'

def deploy():
    site_folder = f'/home/{env.user}/{env.host}'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    
def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('db', 'public/static', 'virtualenv' 'src'):
        run(f'mkdir -p {site_folder}/{subfolder}')

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_head = local('git log -n 1 --format=%H', capture=True)
    run(f'cd {source_folder} && git reset --hard {current_head}')
    
def _update_settings(source_folder, host):
    # Debug false
    settings_file = source_folder + '/superlists/settings.py'
    sed(settings_file, '\bDEBUG = True\b', 'DEBUG = FALSE')
    sed(settings_file, 
        '\bALLOWED_HOSTS = .+$', 
        f'ALLOWED_HOSTS = ["{host}"]'
    )

    # Secret key
    secret_key_file = f'{source_folder}/secret_key.py'
    if not exists(secret_key_file):
        chars = "abcdefg1234"
        secret_key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{secret_key}"')
    append(settings_file, '\nfrom .secret_key import SECRET_KEY')
    
def _update_virtualenv(source_folder):
    virtualenv = f'{source_folder}/../virtualenv'
    if not exists(f'{virtualenv}/bin/pip'):
        run(f'python3 -m venv {virtualenv}')
    run(f'{virtualenv}/bin/pip install -r {source_folder}/requirements.txt')

def _update_static(source_folder):
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput'
    )
    
def _update_database(source_folder):
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py migrate --noinput'
    )
    