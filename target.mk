PYTHON:=python3
VERKADA_API_KEY:=$(VERKADA_API_KEY)
FLAGS:=--verbose
TARGET:=src/main.py

all:
	$(PYTHON) $(TARGET) $(FLAGS)
