from setuptools import setup

requires = ['jinja2 >= 2.7', 'pygments',
            'markdown', 'pyyaml', 'beautifulsoup4']

entry_points = {
    'console_scripts': [
        'urubu = urubu.main:main',
    ]
}

setup(
    name="urubu",
    version="0.9.0",
    url='http://urubu.jandecaluwe.com',
    author='Jan Decaluwe',
    author_email='jan@jandecaluwe.com',
    description="A micro CMS for static websites with a focus "
                "on good navigation practices.",
    packages=['urubu'],
    include_package_data=True,
    install_requires=requires,
    entry_points=entry_points,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
