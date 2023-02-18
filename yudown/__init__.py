"""Top-level package for YuDownloader."""
# yudownloader/__init__.py
from pathlib import Path

from tinydb import Query, TinyDB

__app_name__ = "YuDown"
__version__ = "0.5.0"

yudown_dir = Path.home()/"YuDown"
video_dir = yudown_dir/"Video"
audio_dir = yudown_dir/"Audio"
playlist_dir = yudown_dir/"Playlist"
not_spec_dir = yudown_dir/"notSpecified"

if not Path.exists(yudown_dir):
    Path(yudown_dir).mkdir(exist_ok=True)
    
if not Path.exists(video_dir):
    Path(video_dir).mkdir(exist_ok=True)
    
if not Path.exists(audio_dir):
    Path(audio_dir).mkdir(exist_ok=True)
    
if not Path.exists(playlist_dir):
    Path(playlist_dir).mkdir(exist_ok=True)
    
if not Path.exists(not_spec_dir):
    Path(not_spec_dir).mkdir(exist_ok=True)

db = TinyDB(yudown_dir/"history.json")
db.default_table_name = 'media-history'
MediaQuery = Query()