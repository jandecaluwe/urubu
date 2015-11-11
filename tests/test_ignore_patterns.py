import os
from urubu import project

from . import cd

def test_ignore_patterns():
    with cd('ignore_patterns'):
        project.build()
        assert not os.path.exists(os.path.join('_build', 'README.html'))
        assert os.path.exists(os.path.join('_build', 'page.html'))
