#!/usr/bin/python3
"""a module to generate a tgz archive"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """generates a .tgz archive"""
    local('mkdir -p versions')

    ar = 'web_static_{}.tgz'.format(datetime.now().strftime("%Y%m%d%H%M%S"))
    ar_path = 'versions/' + ar

    res = local('tar -cvfz {} web_static'.format(ar_path))

    if res.succeeded:
        return ar_path
