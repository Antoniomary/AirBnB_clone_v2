#!/usr/bin/python3
"""a module that defines the do_deploy function"""
from fabric.api import local, env, put, run
from os import path
from datetime import datetime


env.hosts = ['100.25.155.10', '54.90.5.78']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """generates a .tgz archive"""
    local('mkdir -p versions')

    ar = 'web_static_{}.tgz'.format(datetime.now().strftime("%Y%m%d%H%M%S"))
    ar_path = 'versions/' + ar

    res = local('tar -cvzf {} web_static'.format(ar_path))

    if res.succeeded:
        return ar_path


def do_deploy(archive_path):
    """distributes an archive to a web server"""
    if not path.exists(archive_path):
        return False

    try:
        # uploads archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        fil = archive_path.split('/')[-1]
        dr = fil[:-4]

        # uncompressing the archive to a new directory on webserver
        new_dir = '/data/web_static/releases/{}'.format(dr)
        run('mkdir -p {}/'.format(new_dir))
        run('tar -xzf /tmp/{} -C {}/'.format(fil, new_dir))

        # delete archive from the web server
        run('rm /tmp/{}'.format(fil))

        # move files
        run('mv {}/web_static/* {}/'.format(new_dir, new_dir))

        # delete folder from which files were moved
        run('rm -rf {}/web_static'.format(new_dir))

        # delete old symlink
        run('rm -rf /data/web_static/current')

        # creates a new symbolic link
        run('ln -s {} /data/web_static/current'.format(new_dir))
    except BaseException:
        return False

    return True
