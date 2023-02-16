"""Top-level package for YuDownloader."""
# yudownloader/__init__.py
import os
from os.path import expanduser

from tinydb import Query, TinyDB

__app_name__ = "YuDown"
__version__ = "0.3.0"

home = expanduser("~")
yudown_dir = home+"/YuDown"
video_dir = yudown_dir+"/video"
audio_dir = yudown_dir+"/audio"
playlist_dir = yudown_dir+"/playlist"
not_spec_dir = yudown_dir+"/notSpecified"

if not os.path.exists(yudown_dir):
    os.makedirs(yudown_dir, exist_ok=True)
    
if not os.path.exists(video_dir):
    os.makedirs(video_dir, exist_ok=True)
    
if not os.path.exists(audio_dir):
    os.makedirs(audio_dir, exist_ok=True)
    
if not os.path.exists(playlist_dir):
    os.makedirs(playlist_dir, exist_ok=True)
    
if not os.path.exists(not_spec_dir):
    os.makedirs(not_spec_dir, exist_ok=True)

db = TinyDB(yudown_dir+"/history.json")
db.default_table_name = 'media-history'
MediaQuery = Query()