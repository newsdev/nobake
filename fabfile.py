import datetime
import json
import os
import time

from fabric import api, operations, contrib
from fabric.state import env

ENVIRONMENTS = {
    "prd-west": {
        "hosts": 'int-elex-prd-west.newsdev.net',
    },
    "prd": {
        "hosts": 'int-elex-prd-east.newsdev.net',
    },
    "stg-west": {
        "hosts": 'int-elex-stg-west.newsdev.net',
    },
    "stg": {
        "hosts": 'int-elex-stg-east.newsdev.net',
    }
}

env.project_name = 'nobake'
env.user = "ubuntu"
env.forward_agent = True
env.branch = "master"

env.hosts = ['127.0.0.1']
env.dbs = ['127.0.0.1']
env.settings = None

@api.task
def development():
    """
    Work on development branch.
    """
    env.branch = 'development'

@api.task
def master():
    """
    Work on stable branch.
    """
    env.branch = 'master'

@api.task
def branch(branch_name):
    """
    Work on any specified branch.
    """
    env.branch = branch_name

@api.task
def e(environment):
    env.settings = environment
    env.hosts = ENVIRONMENTS[environment]['hosts']

@api.task
def clone():
    api.run('git clone git@github.com:newsdev/%(project_name)s.git /home/ubuntu/%(project_name)s' % env)

@api.task
def pull():
    api.run('cd /home/ubuntu/%(project_name)s; git fetch; git pull origin %(branch)s' % env)

@api.task
def pip_install():
    api.run('cd /home/ubuntu/%(project_name)s; workon %(project_name)s && pip install -r py2.requirements.txt' % env)

@api.task
def bounce():
    api.run('sudo service %(project_name)s stop' % env)
    time.sleep(1)
    api.run('sudo service %(project_name)s start' % env)

@api.task
def deploy():
    pull()
    pip_install()
    bounce()
