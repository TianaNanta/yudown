from typing import List
from yudown.model import Media
from yudown import db, MediaQuery

def change_id(old_id: int, new_id: int) -> None:
    db.update({'id': new_id},
              MediaQuery.id == old_id)

def create(media: Media) -> None:
    count = len(db)            
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
    
    if count > 10:
        db.remove(MediaQuery.id == 1)
        for pos in range(2, count):
            change_id(pos, pos-1)

def read() -> List[Media]:
    results = db.all()
    media = []
    for result in results:
        new_media = Media(result['filename'], result['extension'], result['resolution'],
                              result['link'], result['date_downloaded'], result['id'])
        media.append(new_media)
    return media

def destroy() -> None:
    db.drop_tables()