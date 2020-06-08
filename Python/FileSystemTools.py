
import os


def copy_file(source, destination):

    if not os.path.isfile(source):
        raise IOError('Given `source` file path is invalid.')

    dst_dir, _ = os.path.split(destination)
    if not os.path.isdir(dst_dir):
        os.mkdir(dst_dir)

    with open(source, 'rb') as f1, open(destination, 'wb') as f2:
        f2.write(f1.read())


def copy_directory(source, destination, recursive=True):

    if not os.path.isdir(source):
        raise IOError('Given `source` directory is invalid.')

    if not os.path.isdir(destination):
        os.mkdir(destination)

    for item_name in os.listdir(source):

        src_path = os.path.join(source, item_name)
        dst_path = os.path.join(destination, item_name)

        if os.path.isfile(src_path):
            with open(src_path, 'rb') as f1, open(dst_path, 'wb') as f2:
                f2.write(f1.read())

        elif recursive and os.path.isdir(src_path):
            copy_directory(src_path, dst_path)


if __name__ == '__main__':

    copy_directory(
        r"C:\Users\joshuab\Desktop\memes",
        r"C:\Users\joshuab\Desktop\memes2"
    )
