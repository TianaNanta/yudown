from typing import List
from yudown.model import Media
from yudown import db, MediaQuery

def create(media: Media) -> None:
    media.id = len(db)+1
    new_media = {
        'filename': media.filename,
        'extension': media.extension,
        'resolution': media.resolution,
        'link': media.link,
        'date_downloaded': media.date_downloaded,
        'id': media.id
    }
    db.insert(new_media)

def read() -> List[Media]:
    results = db.all()
    media = []
    for result in results:
        new_media = Media(result['filename'], result['extension'], result['resolution'],
                              result['link'], result['date_downloaded'], result['id'])
        media.append(new_media)
    return media

def change_id(old_id: int, new_id: int) -> None:
    db.update({'id': new_id},
              MediaQuery.id == old_id)

def delete(id) -> None:
    count = len(db)
    db.remove(MediaQuery.id == id)
    for pos in range(id+1, count):
        change_id(pos, pos-1)