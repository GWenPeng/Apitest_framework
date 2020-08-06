import tarfile


def untar(filename, path):
    """

    :param filename:
    :param path:
    :return: true
    """
    try:
        t = tarfile.open(filename)
        t.extractall(path=path)
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    untar(filename="response.tar.gz", path="./")
