# Package for media summary database
import os
import sqlite3
import toml
import subprocess
import json

DB_FILE = "mediasummary.sqlite"

def connect():
  if not os.path.isfile(DB_FILE):
    create_db()

  return sqlite3.connect(DB_FILE)

def disconnect(db):
  db.close()

def contains(db, full_name):
  cursor = db.execute(f'SELECT full_name FROM summary WHERE full_name = "{full_name}"')
  if cursor.rowcount == 1:
    return True
  else:
    return False

def add(db, full_name, short_name, date, length, size):
  db.execute(f'''
    INSERT INTO summary (
      "{full_name}",
      "{short_name}",
      "{date}",
      "{length}",
      "{size}",
    )
  ''')

def create_db():
  if not os.path.isfile(DB_FILE):
    db = sqlite3.connect(DB_FILE)

    db.execute('''
      CREATE TABLE "summary" (
        "full_name" TEXT NOT NULL COLLATE NOCASE,
        "short_name" TEXT NOT NULL COLLATE NOCASE,
        "date" INTEGER NOT NULL,
        "length" INTEGER NOT NULL,
        "size" INTEGER NOT NULL
      )
    ''')

    db.close()

def manual_summary(count, total_size, total_length, oldest_title,
  oldest_short, oldest_length, oldest_age):

  result = {}
  result['count'] = count
  result['length'] = total_length
  result['size'] = total_size

  oldest = {}
  oldest['title'] = oldest_title
  oldest['short'] = oldest_short
  oldest['age'] = oldest_age
  oldest['length'] = oldest_length

  result['oldest'] = oldest

  return result

def upload(summary, name):
  with open('summary.toml') as f: config = toml.load(f)
  filename = os.path.join(config['server']['directory'], f'{name}.json')
  cmd = ['ssh', config['server']['connection_string'], f'cat - > {filename}']
  p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
  p.communicate(json.dumps(summary).encode(encoding = 'UTF-8', errors = 'strict'))