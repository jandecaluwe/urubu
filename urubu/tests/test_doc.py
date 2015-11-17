import os

from sh import git, touch
from urubu import project, UrubuError

from urubu.tests import cd

def test_doc():
    with cd('../../doc'):
        project.build()
        touch('_build/.nojekyll')
        d = git('--no-pager', 'diff', '--', '_build')
        if d:
            print(d)
            raise ValueError('Diffs in website')

test_doc()



