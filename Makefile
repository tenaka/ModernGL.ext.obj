ifeq ($(OS), Windows_NT)
	PYTHON = python
else
	PYTHON = python3
endif

all:
	$(PYTHON) -m pip install -U .
