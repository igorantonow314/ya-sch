install:
	python -m pip install -r requirements.txt
	python -m pip install -r requirements-dev.txt

lint:
	python -m black .
	python -m flake8

test:
	./unit_test.sh
