import os
from enum import Enum

from typing import List, Tuple, Callable

from    urllib.parse   import urlsplit, urlunsplit
from    urllib.request import urlretrieve, urlopen
import  tarfile
from    tempfile       import TemporaryDirectory

class Result(Enum):
    PASS    = 'pass'
    FAIL    = 'fail'

TestResult = Tuple[Result, str]

Path = str
Url  = str

SingleTest = Callable[[Path], TestResult]
MultiTest  = Callable[[List[Path]], TestResult]

def test_single_file(test: SingleTest) -> MultiTest:
    """
    runs a test on single file
    """
    def test_file(filenames: List[Path]) -> TestResult:
        try: filename = filenames[0]
        except IndexError: return (Result.FAIL, "No file submitted!")
        return test(filename)

    return test_file


def perform_tests(files_url: Url, feedback_url: Url, test: MultiTest) -> None:
    """
    Downloads the files, runs the test function on each file,
    and sends the feedback to the server.
    """
    res, msg = test_from_url(url_to_fire(files_url), test)
    send_feedback(res, msg, url_to_fire(feedback_url))


def test_from_url(url: Url, test: MultiTest) -> TestResult:
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

def send_feedback(result: Result, msg: str, feedback_url: Url) -> None:
    url = f'{feedback_url}?status={result.value}'
    print(f"#### sending feedback to url {url} ######")
    urlopen(url, bytearray(msg, 'utf-8'))

def url_to_fire(url: Url) -> Url:
    """
    Converts a url so that the host is 'fire', letting us communiate
    to the fire service within the container instead of going via
    the internet
    """
    parts = list(urlsplit(url))
    parts[1] = 'fire:5000'
    return urlunsplit(parts)
