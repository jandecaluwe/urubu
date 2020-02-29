GH-PAGES = ${HOME}/dev/urubu-gh-pages/

all: build

build:
	python3 -m urubu build

serve:
	python3 -m urubu serve

publish:
	cd ..; git subtree push --prefix doc/_build origin gh-pages    
