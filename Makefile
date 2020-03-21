CWD    = $(CURDIR)
MODULE = $(notdir $(CWD))

PIP = $(CWD)/bin/pip3
PY  = $(CWD)/bin/python3


.PHONY: all
all: $(PY) ./$(MODULE).py $(MODULE).ini
	$^



.PHONY: doxy
doxy: doxy.gen
	rm -rf $(CWD)/docs ; doxygen doxy.gen 1>/dev/null



.PHONY: install
install: os $(PIP)
	$(PIP) install    -r requirements.txt
	$(MAKE) requirements.txt

.PHONY: update
update: os $(PIP)
	$(PIP) install -U -r requirements.txt
	$(MAKE) requirements.txt

$(PIP) $(PY):
	python3 -m venv .
	$(CWD)/bin/pip3 install -U pip pylint autopep8

.PHONY: requirements.txt
requirements.txt: $(PIP)
	$< freeze | grep -v 0.0.0 > $@

.PHONY: os
ifeq ($(OS),Windows_NT)
os: windows
else
os: debian
endif

.PHONY: debian
debian:
	sudo apt update
	sudo apt install -u python3 python3-venv
