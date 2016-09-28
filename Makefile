init:
	python core/main.py ${INPUT}

install:
	pip install -r requirements

profile:
	python -m cProfile -s 'tottime' core/main.py ${INPUT} 

test:
	python -m tests.testMaxCut

