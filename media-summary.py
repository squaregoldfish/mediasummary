#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import math
import sys,cgi,cgitb
import traceback
import json
cgitb.enable(display=0, logdir="./cgitb.log")

def frame(text, icon):
  return {'text': text, 'icon': ''.join(['i', str(icon)])}

error = None
count = None
time = None
size = None
days = None
oldest_title = None
oldest_time = None

arguments = cgi.FieldStorage()
source = arguments.getvalue('source')
icon = arguments.getvalue('icon')

if source is None:
  error = 'Missing media source'
elif icon is None:
  error = 'Missing media icon'
else:
  with open(''.join([source, '.json'])) as f:
    data = json.load(f)

    # Episodes
    count = data['count']

    # Total Time
    seconds = data['length']
    hours = int(math.floor(seconds / 3600))
    minutes = int(math.floor(seconds % 3600 / 60))
    time = ':'.join([str(hours), '{0:02d}'.format(minutes)])

    # Size
    size = data['size']
    mb = size / 1024768
    gb = size / 1073742000

    if gb > 1:
      size = '{0:.1f}G'.format(gb)
    else:
      size = '{0:.1f}M'.format(mb)

    # Oldest age
    days = data['oldest']['age']

    oldest_title = data['oldest']['title']

    oldest_time = data['oldest']['length']

    hours = int(math.floor(oldest_time / 3600))
    minutes = int(math.floor(oldest_time % 3600 / 60))
    seconds = oldest_time - (hours * 3600) - (minutes * 60)

    oldest_time = ''
    if hours > 0:
      oldest_time += str(hours)
      oldest_time += ':'

    oldest_time += '{0:02d}:{1:02d}'.format(minutes, seconds)

frames = []

if error is not None:
  frames.append(frame(error, 4786))
else:
  frames.append(frame(''.join(['E ', str(count)]), icon))
  frames.append(frame(time, icon))
  frames.append(frame(size, icon))
  frames.append(frame(''.join(['D ', str(days)]), icon))
  frames.append(frame(''.join([oldest_title, ' (', oldest_time, ')']), icon))

sys.stdout.write('Content-type: application/json\n\n')
sys.stdout.write(json.dumps({"frames": frames}))

