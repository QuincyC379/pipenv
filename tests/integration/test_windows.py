import os

from pipenv.project import Project
from pipenv.vendor import pathlib2 as pathlib

import pytest


# This module is run only on Windows.
pytestmark = pytest.mark.skipif(os.name != 'nt', reason="only relevant on windows")


@pytest.mark.project
def test_case_changes_windows(PipenvInstance, pypi):
    """Test project matching for case changes on Windows.
    """
    with PipenvInstance(pypi=pypi, chdir=True) as p:
        c = p.pipenv('install pytz')
        assert c.return_code == 0

        virtualenv_location = Project().virtualenv_location
        target = p.path.upper()
        if target == p.path:
            target = p.path.lower()
        os.chdir('..')
        os.chdir(target)
        assert os.path.abspath(os.curdir) != p.path

        venv = p.pipenv('--venv').out
        assert venv.strip().lower() == virtualenv_location.lower()


@pytest.mark.files
def test_local_path_windows(PipenvInstance, pypi):
    whl = (
        pathlib.Path(__file__).parent.parent
        .joinpath('pypi', 'six', 'six-1.11.0-py2.py3-none-any.whl')
    )
    try:
        whl = whl.resolve()
    except OSError:
        whl = whl.absolute()
    with PipenvInstance(pypi=pypi, chdir=True) as p:
        c = p.pipenv('install "{0}"'.format(whl))
        assert c.return_code == 0


@pytest.mark.files
def test_local_path_windows_forward_slash(PipenvInstance, pypi):
    whl = (
        pathlib.Path(__file__).parent.parent
        .joinpath('pypi', 'six', 'six-1.11.0-py2.py3-none-any.whl')
    )
    try:
        whl = whl.resolve()
    except OSError:
        whl = whl.absolute()
    with PipenvInstance(pypi=pypi, chdir=True) as p:
        c = p.pipenv('install "{0}"'.format(whl.as_posix()))
        assert c.return_code == 0
