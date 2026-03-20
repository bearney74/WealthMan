ruff:
	ruff check
	ruff format

test: unittests

unittest: unittests

unittests:
	python -m unittest discover --verbose -s tests -t . -p *_test.py
