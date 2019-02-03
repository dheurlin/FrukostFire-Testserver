from flask import Flask

from typing import List, Tuple, Callable

import os
from enum import Enum

from    urllib.parse   import urlsplit, urlunsplit
from    urllib.request import urlretrieve, urlopen
import  tarfile
from    tempfile       import TemporaryDirectory
import  yaml

app = Flask(__name__)

class Result(Enum):
    PASS    = 'pass'
    FAIL    = 'fail'

TestResult = Tuple[Result, str]

SingleTest = Callable[[str], TestResult]
MultiTest = Callable[[List[str]], TestResult]

@app.route('/application/<path:files_url>/feedback/<path:feedback_url>')
def application(files_url, feedback_url):
    perform_tests(files_url, feedback_url, test_single_file(validate_application))
    return "Running tests"

def validate_application(filename: str) -> TestResult:
    """
    Validates the sittning application. Expecting filename to refer to a yaml file
    """
    class Field():
        def __init__(self, name: str, required: bool = False):
            self.name = name
            self.required = required

    fields = {Field('namn', required=True), Field('matgnäll'), Field('gdpr', required=True)}

    with open(filename) as f:
        try: data = yaml.load(f)
        except yaml.YAMLError as e:
            return (Result.FAIL, f'Invalid syntax in submitted file! \n\n {str(e)}')
        except Exception as e:
            return (Result.FAIL, f'Something went wrong! {str(e)}')

    missing = []
    for field in fields:
        if (field.name not in data or not data[field.name]) and field.required:
            missing.append(field.name)

    if not len(missing) == 0:
        return (Result.FAIL, "Missing required fields: \n" + "\n".join(missing))


    # TODO verify GDPR

    return (Result.PASS, str(data))

def test_single_file(test: SingleTest) -> MultiTest:
    """
    runs a test on single file
    """
    def test_file(filenames: List[str]) -> TestResult:
        try: filename = filenames[0]
        except IndexError: return (Result.FAIL, "No file submitted!")
        return test(filename)

    return test_file


def perform_tests(files_url: str, feedback_url: str, test: MultiTest) -> None:
    """
    Downloads the files, runs the test function on each file,
    and sends the feedback to the server.
    """
    res, msg = test_from_url(url_to_fire(files_url), test)
    send_feedback(res, msg, url_to_fire(feedback_url))


def test_from_url(url: str, test: MultiTest) -> TestResult:
    """
    Downloads and unpacks the url, and performs the test
    """
    with TemporaryDirectory() as arch_dir, TemporaryDirectory() as files_dir:
        arch_path = os.path.join(arch_dir, 'archive.tar.gz')
        print(f"#### downloading from url {url} ######")
        urlretrieve(url, arch_path)
        with tarfile.open(arch_path) as tar:
            tar.extractall(files_dir)

        fullpaths = list(map(lambda f: os.path.join(files_dir, f), os.listdir(files_dir)))
        return test(fullpaths)

def send_feedback(result: Result, msg: str, feedback_url: str) -> None:
    url = f'{feedback_url}?status={result.value}'
    print(f"#### sending feedback to url {url} ######")
    urlopen(url, bytearray(msg, 'utf-8'))

def url_to_fire(url: str) -> str:
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
