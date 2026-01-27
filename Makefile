PYTHON:=python3
VERKADA_API_KEY:=$(VERKADA_API_KEY)
FLAGS:=--verbose --verkada-api-key=$(VERKADA_API_KEY)
TARGET:=src/main.py

all:
	$(PYTHON) $(TARGET) $(FLAGS)
