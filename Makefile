install:
	python -m pip install -r requirements.txt
	python -m pip install -r requirements-dev.txt

lint:
	python -m black . --exclude unit_test.py
	python -m flake8

test:
	python -m pytest tests/
	./unit_test.sh
