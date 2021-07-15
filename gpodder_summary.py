# Build media summary from GPodder database
import toml
import sqlite3
from datetime import datetime
import summary

# SQL query for GPodder database
GPODDER_SQL = 'select p.title, e.title, e.download_filename, e.file_size, e.total_time, e.published from podcast p inner join episode e on e.podcast_id = p.id where e.state=1 order by e.published asc'

# Load configuration
with open('gpodder.toml') as f: config = toml.load(f)

# Load gpodder database
gpodder_db = sqlite3.connect(config['gpodder']['db'])
cursor = gpodder_db.cursor()
cursor.execute(GPODDER_SQL)

# Output info
count = 0
total_length = 0
total_size = 0
oldest_title = None
oldest_short = None
oldest_age = None
oldest_length = 0


for row in cursor:
  count += 1

  podcast = row[0]
  episode = row[1]
  filename = row[2]
  size = row[3]
  if size < 0:
    size = 0

  length = row[4]
  if length < 0:
    length = 0

  date = row[5]

  if count == 1:
    oldest_title = f'{podcast}: {episode}'
    oldest_short = f'{podcast}: {filename}'
    oldest_age = (datetime.now() - datetime.fromtimestamp(date)).days
    oldest_length = length

  total_length += length
  total_size += size

gpodder_db.close()

result = summary.manual_summary(count, total_size, total_length, oldest_title,
  oldest_short, oldest_length, oldest_age)

with open('oldest.txt', 'w') as f:
  f.write(result['oldest']['short'])

summary.upload(result, 'podcasts')