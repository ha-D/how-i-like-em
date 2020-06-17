#!/usr/bin/env python3

from subprocess import run
import argparse
import sys
import json
import threading

default_state = {
    'current': 'default',
    'activities': {
        'default': []
    }
}

def get_windows(space=None):
    cmd = ['query', '--windows']
    if space is not None:
        cmd += ['--space', str(space)]
    return json.loads(yabai(*cmd))

def get_spaces(space=None):
    cmd = ['query', '--windows']
    if space is not None:
        cmd += ['--space', str(space)]
    return json.loads(yabai(*cmd))

def yabai(*cmds):
    res = run(['yabai', '-m', *[str(s) for s in cmds]], capture_output=True)
    if res.returncode != 0:
        sys.stderr.write(res.stderr.decode('utf-8'))
        sys.stderr.write('\n')
        raise ValueError(f'Invalid return code {res.returncode}')
    return res.stdout.decode('utf-8')

def load_state():
    try:
        with open('.switcher.json', 'r') as f:
            return json.loads(f.read())
    except:
        print('failed to load state, using default state')
        return default_state

def save_state(state):
    with open('.switcher.json', 'w') as f:
        return f.write(json.dumps(state))

def clear_activity():
    for window in get_windows():
        if window['native-fullscreen'] == 1:
            yabai('window', window['id'], '--toggle', 'native-fullscreen')
 
        if window['minimized'] != 1:
            yabai('window', window['id'], '--minimize')

    while True:
        try: yabai('space', '--destroy')
        except: break


def restore_activity(windows):
    space_count = 1
    for w in windows:
        try:
            yabai('window', w['id'], '--deminimize')
            while w['space'] > space_count:
                yabai('space', '--create')
                space_count += 1
            yabai('window', w['id'], '--space', w['space'])
        except Exception as e:
            print("failed to restore window", w['id'], w['app'], w['title'])
            print(e)

    for w in windows:
        try:
            if w['native-fullscreen'] == 1:
                yabai('window', w['id'], '--toggle', 'native-fullscreen')
        except Exception as e:
            print(e)

    for w in windows:
        try:
            if w['native-fullscreen'] == 1:
                yabai('space', w['space'], '--destroy')
        except Exception as e:
            print(e)

parser = argparse.ArgumentParser()
parser.add_argument("name")
args = parser.parse_args()

state = load_state()

state['activities'][state['current']] = [w for w in get_windows() if w['minimized'] != 1]
state['current'] = args.name
save_state(state)


clear_activity()
restore_activity(state['activities'].get(args.name, []))


