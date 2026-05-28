PYTHON ?= python3

.PHONY: test run-local tree

test:
	$(PYTHON) -m pytest

run-local:
	$(PYTHON) scripts/run_local.py --config configs/dev.yaml

tree:
	find . -maxdepth 3 -type f | sort

