from flask import Flask

import os
from contextlib import contextmanager
from enum import Enum

from urllib.parse   import urlsplit, urlunsplit
from urllib.request import urlretrieve, urlopen
import tarfile
from tempfile import TemporaryDirectory

app = Flask(__name__)

class Result(Enum):
    PASS    = 'pass'
    FAIL    = 'fail'

@app.route('/application/<path:files_url>/feedback/<path:feedback_url>')
def application(files_url, feedback_url):
    msg = lambda txt : """
    My feedback: the file was called """ + str(txt) + """

    This submission was quite gay. However,

    it is not wrong to be gay, since it is the current year.
    Hence you pass the assignment
    """
    perform_tests(files_url, feedback_url, lambda files: (Result.PASS, msg("".join(files))))
    return "Running tests"


def perform_tests(files_url, feedback_url, test):
    """
    Downloads the files, runs the test : [file] -> (result : Result, msg : String)
    function on each file, and sends the feedback to the server.
    """
    res, msg = test_from_url(url_to_fire(files_url), test)
    send_feedback(res, msg, url_to_fire(feedback_url))


def test_from_url(url, test):
    """
    Downloads and unpacks the url, and performs the test
    """
    with TemporaryDirectory() as arch_dir, TemporaryDirectory() as files_dir:
        arch_path = os.path.join(arch_dir, 'archive.tar.gz')
        print(f"#### downloading from url {url} ######")
        urlretrieve(url, arch_path)
        with tarfile.open(arch_path) as tar:
            tar.extractall(files_dir)

        return test(os.listdir(files_dir))

def send_feedback(result, msg, feedback_url):
    url = f'{feedback_url}?status={result.value}'
    print(f"#### sending feedback to url {url} ######")
    urlopen(url, bytearray(msg, 'utf-8'))

def url_to_fire(url):
    """
    Converts a url so that the host is 'fire', letting us communiate
    to the fire service within the container instead of going via
    the internet
    """
    parts = list(urlsplit(url))
    parts[1] = 'fire:5000'
    return urlunsplit(parts)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=14500)
