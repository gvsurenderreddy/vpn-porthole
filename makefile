develop:
	./setup.sh


test:
	trial tests/test_*.py


coverage:
	coverage run tests/test_types.py
	coverage html
	open htmlcov/index.html


clean:
	rm -rf build
	rm -rf _trial*
	rm -rf htmlcov


analyse:
	find VPNPorthole -name '*.py' | xargs pep8 --ignore E501
	find VPNPorthole -name '*.py' | xargs pyflakes
	find VPNPorthole -name '*.py' | xargs pylint -d invalid-name -d locally-disabled -d missing-docstring -d too-few-public-methods -d protected-access


metrics:
	find VPNPorthole -name '*.py' | xargs radon cc -s -a -nb
	find VPNPorthole -name '*.py' | xargs radon mi -s


to_pypi_test:
	python setup.py register -r pypitest
	python setup.py sdist upload -r pypitest


to_pypi_live:
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi
