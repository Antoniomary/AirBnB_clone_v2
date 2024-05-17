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
        return

    if number <= 1:
        number = 2
    else:
        number += 1

    local('ls -1t versions/ | tail +{} | xargs rm'.format(number))
    # run('ls -1t /data/web_static/releases | tail +{} | xargs rm'.format(number))
