import os


class MapRoot:
    def __init__(self, root: str):
        self.root = root
        self._tree = []

    
    def tree(self) -> list:
        dirs = []
        files = []

        for i in os.listdir(self.root):
            if os.path.isdir(self.root + "/" + i):
                dirs.append(self.root + "/" + i)

            else:
                files.append(self.root + "/" + i)


        for d in dirs:
            files += MapRoot(d).tree()

        self._tree += files

        return self._tree

        