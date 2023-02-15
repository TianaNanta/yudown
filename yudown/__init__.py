"""Top-level package for YuDownloader."""
# yudownloader/__init__.py
import os
from os.path import expanduser

from tinydb import Query, TinyDB

__app_name__ = "YuDown"
__version__ = "0.1.0"
home = expanduser("~")
yudown_dir = home+"/YuDown"

if not os.path.exists(yudown_dir):
    os.makedirs(yudown_dir, exist_ok=True)

db = TinyDB(yudown_dir+"/history.json")
db.default_table_name = 'media-history'
MediaQuery = Query()