PYTHON:=python3
FLAGS:=--verbose --output-log='target.log'
TARGET:=src/main.py

all:
	$(PYTHON) $(TARGET) $(FLAGS)

clean:
	rm target.log
