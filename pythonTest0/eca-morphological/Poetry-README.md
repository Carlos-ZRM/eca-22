## Install pyenv
~~~ bash
pyenv install 3.13
pyenv local 3.13
~~~

## Use poetry
~~~ bash


poetry env list
poetry env use python3.13
~~~


~~~ bash
poetry env info

Virtualenv
Python:         3.13.5
Implementation: CPython
Path:           /Users/creyesma/Library/Caches/pypoetry/virtualenvs/eca-morphological-xOIbiyJH-py3.13
Executable:     /Users/creyesma/Library/Caches/pypoetry/virtualenvs/eca-morphological-xOIbiyJH-py3.13/bin/python
Valid:          True

Base
Platform:   darwin
OS:         posix
Python:     3.13.5
Path:       /opt/homebrew/opt/python@3.13/Frameworks/Python.framework/Versions/3.13
Executable: /opt/homebrew/opt/python@3.13/Frameworks/Python.framework/Versions/3.13/bin/python3.13
~~~

## Poetry add packages

~~~ bash
poetry add --group dev ruff pylint isort pre-commit
~~~

## Run commands

~~~ bash
poetry run isort .
~~~

~~~ bash
poetry run ruff check .
poetry run ruff check . --fix --unsafe-fixes
~~~

~~~ bash
poetry run pylint src/*
~~~

## RUN app

~~~ bash
poetry run python3 src/app.py
~~~


## Note config Pylint
Add follow lines `.pylintrc` to prevent erros
~~~ bash
************* Module ca_mm_object
src/ca_mm_object.py:57:14: E1101: Module 'cv2' has no 'imread' member (no-member)
src/ca_mm_object.py:58:19: E1101: Module 'cv2' has no 'dilate' member (no-member)
~~~~

~~~ toml

[MESSAGES CONTROL]
...
disable=raw-checker-failed,
...
        maybe-no-member
~~~
