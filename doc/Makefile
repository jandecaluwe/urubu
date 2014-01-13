GH-PAGES = ${HOME}/dev/urubu-gh-pages/

all: build

build:
	python -m urubu build

serve:
	cd _build; python -m urubu serve

publish:
	rsync -avr --exclude '.*' --delete _build/ ${GH-PAGES}    
