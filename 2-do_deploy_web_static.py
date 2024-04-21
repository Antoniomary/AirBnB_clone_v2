#!/usr/bin/python3
"""Compress web static package"""
from fabric.api import *
from os import path


env.hosts = ['52.91.119.206', '35.153.83.163']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Function that will run the script."""
    if not os.path.exists(archive_path):
        return False
    put(archive_path, "/tmp/")
    compressed_filepath = "versions/web_static_20230406235730.tgz"
    compressed_filename = compressed_filepath.split("/")[1]
    compressed_file_without_ext = compressed_filename.split(".")[0]
    folder_uncompressed_file = "/data/web_static/releases/{}".format(
        compressed_file_without_ext)
    run("sudo mkdir -p {}".format(folder_uncompressed_file))
    run("sudo tar -xzf /tmp/{} -C {}".format(
        compressed_filename, folder_uncompressed_file))
    run("sudo rm /tmp/{} ".format(compressed_filename))
    run("sudo mv {}/web_static/* {}".format(
        folder_uncompressed_file, folder_uncompressed_file))
    run("sudo rm -rf {}/web_static".format(folder_uncompressed_file))
    run("sudo rm -rf /data/web_static/current")
    run("sudo ln -s {} /data/web_static/current".format(
        folder_uncompressed_file))
    return True
