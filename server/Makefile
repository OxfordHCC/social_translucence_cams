db:
	mkdir db

run:
	source venv/bin/activate ;\
	python3 main.py

venv:
	python3 -m venv ./venv

install: requirements.txt | venv db
	source venv/bin/activate ;\
	python3 -m pip install -r requirements.txt ;\
	python3 init_db.py

test:
	source venv/bin/activate ;\
	python -m pytest

clean:
	rm -r ./venv/

reset_db:
	rm -r ./db/

