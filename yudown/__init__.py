"""Top-level package for YuDownloader."""
# yudownloader/__init__.py
from tinydb import TinyDB, Query


__app_name__ = "YuDown"
__version__ = "0.1.0"


db = TinyDB('media-history.json')
db.default_table_name = 'media-history'
MediaQuery = Query()