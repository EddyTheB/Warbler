import os
import json
homeDir = os.path.expanduser('~')

def getKey(key, file='Default'):
  if file == 'Default':
    file = homeDir + '/.keys/keys'
  with open(file) as df:
    d = json.load(df)
  return d[key]

