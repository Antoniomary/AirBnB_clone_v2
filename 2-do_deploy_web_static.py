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

    try:
        # uploads archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        file = archive_path.split('/')[-1]
        dir = file[:-4]

        # uncompressing the archive to a new directory on webserver
        run('sudo mkdir -p /data/web_static/releases/{}'.format(dir))

        run(f"sudo tar -xzf /tmp/{file} -C /data/web_static/releases/{dir}")

        # delete archive from the web server
        run('sudo rm /tmp/{}'.format(file))

        # move files
        run(f'sudo mv /data/web_static/releases/{dir}/web_static/* \
/data/web_static/releases/{dir}')

        # delete folder from which files were moved
        run(f'sudo rm -rf /data/web_static/releases/{dir}/web_static')

        # delete old symlink
        run('sudo rm -rf /data/web_static/current')

        # creates a new symbolic link
        run(f"sudo ln -s /data/web_static/releases/{dir} \
/data/web_static/current")
    except Exception:
        return False

    return True
