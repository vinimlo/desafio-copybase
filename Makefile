all: init install

init:
	pipenv shell --python python3

install:
	pipenv install --skip-lock
