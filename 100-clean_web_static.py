#!/usr/bin/python3
"""a fabric script that deletes out-of-date archives"""
from fabric.api import env, local, run


env.hosts = ['52.91.119.206', '35.153.83.163']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_clean(number=0):
    """deletes all unnecessary archives"""
    if number < 0:
        return

    if number <= 1:
        number = 2
    else:
        number += 1

    local('ls -1t versions/ | tail +{} | xargs rm'.format(number))
    run('ls -1t /data/web_static/releases | tail +{} | xargs rm'.format(number))
