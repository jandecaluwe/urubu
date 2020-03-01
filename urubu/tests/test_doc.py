import os, sys

from sh import git, touch
from urubu import project, UrubuError

from urubu.tests import cd

def test_doc():
    with cd('../../doc'):
        sys.path.insert(0, os.getcwd())
        project.build()
        touch('_build/.nojekyll')
        d = git('--no-pager', 'diff', '-w', '--', '_build')
        if d:
            print(d)
            raise ValueError('Diffs in website')
    _python = None

test_doc()



