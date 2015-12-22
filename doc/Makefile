GH-PAGES = ${HOME}/dev/urubu-gh-pages/

all: build

build:
	python -m urubu build

serve:
	python -m urubu serve

publish:
	cd ..; git subtree push --prefix doc/_build origin gh-pages    
