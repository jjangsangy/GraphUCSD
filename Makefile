SHELL   := /bin/bash
PROJECT := cape
OSNAME  := $(shell uname -s)
ARCH    := $(shell uname -m)

# Python Information
PYTHON_VERSION := 2
PYTHON  := $(shell which python$(PYTHON_VERSION))
INSTALL := Miniconda$(subst 2,,$(PYTHON_VERSION))-latest-$(subst Darwin,MacOSX,$(OSNAME))-$(ARCH).sh
URL     := http://repo.continuum.io/miniconda/${INSTALL}
CONDA   := conda/bin/conda
PIP     := conda/bin/pip
IPYTHON := conda/bin/ipython
RUN     := conda/bin/python

.PHONY: conda
conda: $(CONDA)
	$(CONDA) update -y conda
	$(CONDA) install -y lxml pandas

	$(PIP) install -r requirements.txt

.PHONY: all run
all: install

.PHONY: help
help:
	@echo " Usage: \`make <target>'"
	@echo " ======================="
	@echo "  serve   run ipython notebook"
	@echo "  conda   boostrap anacondas python"
	@echo "  install boostrap anacondas python"
	@echo "  clean   remove build files"
	@echo
	@echo

$(CONDA):
	@echo "installing conda"
	curl -O $(URL);
	@if  [ -r conda ]; then rm -rf conda; fi
	@bash $(INSTALL) -b -p conda

.PHONY: install
install: conda
	@echo "Packages Installed"

.PHONY: run
run: $(RUN)
	$(RUN) cape.py

$(IPYTHON): conda
serve: $(IPYTHON)
	$(IPYTHON) notebook

slides: $(IPYTHON)
	$(IPYTHON) nbconvert --to slides --post serve cape.ipynb

.PHONY: clean
clean:
	rm -rf .DS_Store
	rm -rf conda
	rm -rf $(INSTALL)
	rm -rf cape.csv
