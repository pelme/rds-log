
class LocalLogFile:
    def __init__(self, root_directory, filename):
        self.filename = filename
        self._root_directory = root_directory
        self._path = self._root_directory / self.filename

    @property
    def size(self):
        try:
            return self._path.stat().st_size
        except FileNotFoundError:
            return -1

    def open_for_write(self):

        try:
            self._path.parent.mkdir(parents=True)
        except FileExistsError:
            pass

        return self._path.open('w+b')
