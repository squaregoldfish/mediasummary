# Video summariser
import summary
import os
import toml
from datetime import datetime
import time
import cv2
import math

def num_dir_list(path):
  dirs = [d for d in os.listdir(path) if d.isnumeric()]
  dirs.sort()
  return dirs

with open('video.toml') as f: config = toml.load(f)
dir = config['videos']['directory']

db = summary.connect()

# Add any new files
for y in num_dir_list(dir):
  for m in num_dir_list(os.path.join(dir, y)):
    folder = '{}/{}'.format(y, m)
    for vid in os.listdir(os.path.join(dir, y, m)):

      full_path = os.path.join(dir, y, m, vid)

      vidpath = os.path.join(y, m, vid)
      if not summary.contains(db, vidpath):
        full_name = vidpath
        short_name = os.path.splitext(os.path.basename(vidpath))[0]

        date = datetime.strptime('{}{}'.format(y, m), '%Y%m%d')
        timestamp = int(time.mktime(date.timetuple()))

        length = 0
        vid = cv2.VideoCapture(full_path)
        fps = vid.get(cv2.CAP_PROP_FPS)
        if fps > 0:
          frame_count = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
          length = int(math.floor(frame_count / fps))

        size = os.path.getsize(full_path)

        summary.add(db, vidpath, short_name, timestamp, length, size)

# Remove any files that no longer exist
db_files = summary.get_all(db)
for file in db_files:
  if not os.path.exists(os.path.join(dir, file[0])):
    summary.remove(db, file[0])

# Make the summary
summary.make_summary(db, 'videos')

summary.disconnect(db)
