from flask import Flask

import os
from contextlib import contextmanager

from urllib.parse   import urlsplit, urlunsplit
from urllib.request import urlretrieve
import tarfile
from tempfile import TemporaryDirectory

app = Flask(__name__)

@app.route('/test/<path:files_url>/feedback/<path:feedback_url>')
def receive_test(files_url, feedback_url):
    files_url = url_to_fire(files_url)
    test_from_url(files_url, lambda _: True)
    return files_url

def test_from_url(url, test):
    """
    Downloads and unpacks the url, and performs the
    test : [file] -> Bool function on each file
    of filesk
    """
    with TemporaryDirectory() as arch_dir, TemporaryDirectory() as files_dir:
        arch_path = os.path.join(arch_dir, 'archive.tar.gz')
        print(f"#### downloading from url {url} ######")
        urlretrieve(url, arch_path)
        with tarfile.open(arch_path) as tar:
            tar.extractall(files_dir)

        for name in os.listdir(files_dir):
            print(name)

def url_to_fire(url):
    """
    Converts a url so that the host is 'fire', letting us communiate
    to the fire service within the container instead of going via
    the internet
    """
    parts = list(urlsplit(url))
    parts[1] = 'fire:5000'
    return urlunsplit(parts)

# @contextmanager
# def changedir(path):
#     """
#     Changes the directory and restores it afterwards
#     """
#     olddir = os.getcwd()
#     os.chdir(path)
#     try: yield
#     finally: os.chdir(olddir)




# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     print(f'################ CATCH-ALL: {path}')
#     return f'########### CATCH_ALL: {path}'


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=14500)
