import datetime

class Media:
    def __init__ (self, filename, extension, resolution, link, date_downloaded=None, id=None):
        self.filename = filename
        self.extension = extension
        self.resolution = resolution
        self.link = link
        self.date_downloaded = date_downloaded if date_downloaded is not None else datetime.datetime.now().isoformat()
        self.id = id

    def __repr__ (self) -> str:
        """Make the class more readeable
        """
        return f"({self.filename}, {self.extension}, {self.resolution}, {self.link}, {self.date_downloaded}, {self.id}"