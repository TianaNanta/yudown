import datetime

class Media:
    def __init__ (self, id, filename, extension, resolution, link, date_downloaded=None):
        self.id = id
        self.filename = filename
        self.extension = extension
        self.resolution = resolution
        self.link = link
        self.date_downloaded = date_downloaded if date_downloaded is not None else datetime.datetime.now().isoformat()

    def __repr__ (self) -> str:
        """Make the class more readeable
        """
        return f"({self.id}, {self.filename}, {self.extension}, {self.resolution}, {self.link}, {self.date_downloaded}"