## FIX

~~~ bash 

poetry run ruff check --fix . --unsafe-fixes

~~~
## RUN app

~~~ bash
poetry run python3 src/app.py
~~~

~~~ bash
poetry run uvicorn src.web-app:app --reload
~~~
