import os

from sh import git 
from urubu import project

from tests import cd

def test_doc():
    with cd('../doc'):
        project.build()
        print git('--no-pager', 'diff')

test_doc()



