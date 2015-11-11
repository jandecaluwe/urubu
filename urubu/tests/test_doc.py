import os

from sh import git 
from urubu import project

from urubu.tests import cd

def test_doc():
    with cd('../../doc'):
        project.build()
        d = git('--no-pager', 'diff')
        print(d)

test_doc()



