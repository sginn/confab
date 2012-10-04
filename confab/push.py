"""
Push generated configuration files to remote host.
"""

from confab.files import get_conf_files, env_from_dir
from confab.generate import generate_conf_files
from confab.pull import pull_conf_files
from confab.options import get_default_options
from fabric.api import abort, env, task

import os

def push_conf_files(conf_files, generated_dir, remotes_dir):

    # XXX diffs, defer push 

    for conf_file in conf_files:
        conf_file.push(generated_dir)

@task
def push(template_dir=None, generated_dir=None, remotes_dir=None):
    """
    Push configuration files.
    """

    if not template_dir or not os.path.isdir(template_dir):
        abort('Please provide a valid template_dir')

    if not generated_dir or (os.path.exists(generated_dir) and not os.path.isdir(generated_dir)):
        abort('Please provide a valid generated_dir')

    if not remotes_dir or (os.path.exists(remotes_dir) and not os.path.isdir(remotes_dir)):
        abort('Please provide a valid remotes_dir')

    if not env.host_string:
        abort('Please specify a host or a role')

    options = get_default_options()
    environment = env_from_dir(template_dir)
    data = {}
    conf_files = get_conf_files(environment, data, options)

    pull_conf_files(conf_files, remotes_dir)
    generate_conf_files(conf_files, generated_dir)
    push_conf_files(conf_files, generated_dir, remotes_dir)
