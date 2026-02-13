ruff:
	ruff format

unittest: unittests

unittests:
	python -m unittest discover --verbose -s tests -t . -p *_test.py
