import os
import sys
import re
sys.path.append(os.path.realpath('.'))
from pprint import pprint

import inquirer
import yaml
import subprocess


with open('setup.yaml') as f:
    config = yaml.safe_load(f.read())[0]


questions = [
    inquirer.Text('host',  message='Enter host'),
    inquirer.Text('user',  message='Enter username', default=config['vars']['ansible_user']),
    inquirer.Text('proxy',  message='Enter proxy'),
    inquirer.Checkbox('roles', message='Select roles', choices=config['roles'])
]

answers = inquirer.prompt(questions)

config['vars']['ansible_user'] = answers['user']
config['vars']['http_proxy'] = answers['proxy']
config['roles'] = answers['roles']

with open('setup.rendered.yaml', 'w') as f:
    f.write(yaml.safe_dump([config]))

command = 'ansible-playbook -i {}, setup.rendered.yaml'.format(answers['host'])

print(command)
process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE)
for c in iter(lambda: process.stdout.read(1), ''):
    sys.stdout.write(c.decode('utf-8'))

