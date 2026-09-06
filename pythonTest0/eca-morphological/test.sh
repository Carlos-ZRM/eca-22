rm *.png
poetry run python  src/app_mm.py
poetry run python  src/app_fra_tcount.py 2&> test-fra-count.log
