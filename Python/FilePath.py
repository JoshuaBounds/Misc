from typing import *
import os


class FilePath(str):

    def __truediv__(self, other: AnyStr) -> 'FilePath':
        return self.__class__(os.path.join(self, other))

    def components(self: AnyStr) -> List[AnyStr]:
        """
        Splits the given path into a list of it's components
        (drive, directories, file name).
        """
        def recurse(p):
            remaining_path, component = os.path.split(p)
            if remaining_path and component:
                result = recurse(remaining_path)
                result.append(component)
                return result
            else:
                return [p]
        return recurse(self)


if __name__ == '__main__':

    a = r"E:\XXX\Mega Milk\MegaMilk_pg1.jpg"
    a = r"E:\XXX\Mega Milk\MegaMilk_pg1.jpg"
    file_path = FilePath(a)
    print(10 / 'a')
