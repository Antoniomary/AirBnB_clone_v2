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
        number = 2
    else:
        number += 1

    archives = local(f'ls -1t versions/ | tail +{number}', capture=True)
    for archive in archives.split('\n'):
        local(f'rm versions/{archive}')

    path = '/data/web_static/releases'
    archives = run(f"find {path} -type d -name 'web_static_*' | xargs ls -1t\
                    | tail +{number}")
    for archive in archives.split('\n'):
        run(f'rm -rf {archive}')
