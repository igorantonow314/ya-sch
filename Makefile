install:
	python -m pip install -r requirements.txt
	python -m pip install -r requirements-dev.txt

lint:
	python -m black . --exclude unit_test.py
	python -m flake8

test:
	# python -m pytest tests/
	python -m coverage run -m pytest
	python -m coverage report --omit="/usr/lib/*"
	python -m coverage html --omit="/usr/lib/*"
	./unit_test.sh
