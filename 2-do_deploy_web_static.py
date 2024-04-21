#!/usr/bin/python3
"""a module that defines the do_deploy function"""
from fabric.api import env, put, run
from os import path


env.hosts = ['52.91.119.206', '35.153.83.163']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """distributes an archive to a web server"""
    if not path.exists(archive_path):
        return False

    # uploads archive to the /tmp/ directory of the web server
    r = put(archive_path, '/tmp/')
    if r.failed:
        return False

    file = archive_path.split('/')[-1]
    dir = file[:-4]

    # uncompressing the archive to a new directory on webserver
    r = run('mkdir -p /data/web_static/releases/{}'.format(dir))
    if r.failed:
        return False
    r = run(f"tar -xzf /tmp/{file} -C /data/web_static/releases/{dir}")
    if r.failed:
        return False

    # delete archive from the web server
    r = run('rm /tmp/{}'.format(file))
    if r.failed:
        return False

    # move files
    r = run(f'mv /data/web_static/releases/{dir}/web_static/* \
            /data/web_static/releases/{dir}')
    if r.failed:
        return False

    # delete folder from which files were moved
    r = run(f'rm -rf /data/web_static/releases/{dir}/web_static')
    if r.failed:
        return False

    # delete old symlink
    r = run('rm -rf /data/web_static/current')
    if r.failed:
        return False

    # creates a new symbolic link
    r = run(f"ln -s /data/web_static/releases/{dir} /data/web_static/current")
    if r.failed:
        return False

    return True
