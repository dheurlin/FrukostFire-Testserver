from flask import Flask

from typing import List, Tuple, Callable
import yaml
import sqlite3

from testing import Result, TestResult, SingleTest, MultiTest, Path
from testing import perform_tests, test_single_file

import db

app = Flask(__name__)


@app.route('/application/<path:files_url>/feedback/<path:feedback_url>')
def application(files_url, feedback_url):
    perform_tests(files_url, feedback_url, test_single_file(validate_application))
    return "Running tests"


def validate_application(filename: Path) -> TestResult:
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

    if not data['gdpr'] == 'ok':
        return (Result.FAIL, "You must answer 'ok' to GDPR to attend. Sorry!")

    namn = data['namn']
    try: gnäll = data['matgnäll']
    except: gnäll = []

    try: db.insert_attendent(namn, gnäll)
    except sqlite3.IntegrityError:
        return (Result.FAIL, f'Du har redan anmält dig, {namn}!')

    return (Result.PASS, f'Välkommen till sittningen, {namn}!')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=14500)
