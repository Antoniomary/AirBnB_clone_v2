#!/usr/bin/python3
"""a fabric script that deletes out-of-date archives"""
from fabric.api import env, local, run
from sys import exit


env.hosts = ['100.25.155.10', '54.90.5.78']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_clean(number=0):
    """deletes all unnecessary archives"""
    try:
        number = int(number)
    except ValueError:
        print("Error: Invalid number")
        exit(1)

    if number < 0:
        exit(1)

    if number <= 1:
        n = 2
    else:
        n = number + 1

    archives = local(f'ls -1t versions/ | tail +{n}', capture=True)
    for archive in archives.split():
        if archive:
            local(f'rm versions/{archive}')

    path = '/data/web_static/releases/*'
    archives = run(f"ls -1dt {path}".strip())
    archives = archives.split()
    if path[:-1] + 'test' in archives:
        archives.remove(path[:-1] + 'test')
    if number == 0:
        number = 1
    for archive in archives[number:]:
        run('rm -rf {}'.format(archive).strip())
