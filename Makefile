PYTHON ?= python3

.PHONY: test run-local run-demo tree

test:
	$(PYTHON) -m pytest

run-local:
	$(PYTHON) scripts/run_local.py --config configs/dev.yaml

run-demo:
	streamlit run streamlit_app.py

tree:
	find . -maxdepth 3 -type f | sort
