.DEFAULT_GOAL := test

UV ?= uv

.PHONY: test build evaluate

# Run Python unit and regression tests with the locked development environment.
test:
	$(UV) run --locked pytest

# Audit both palettes, regenerate every theme port, and refresh README previews.
build:
	$(UV) run --locked python scripts/build.py

# Full native acceptance pipeline; see docs/development.md for one-time prerequisites.
EVALUATE_OUTPUT ?= evaluation/results/full
CODEX_SOURCE ?= ../review-codex
PYTHON_SOURCE ?= ../eval-tree-sitter-python
THEMES ?= ithilien-dawn

evaluate: test
	$(UV) run --locked python scripts/evaluate_suite.py --fresh-run --strict-gates \
		--codex-source "$(CODEX_SOURCE)" --python-source "$(PYTHON_SOURCE)" \
		--output "$(EVALUATE_OUTPUT)" --themes $(THEMES) \
		--pickers --python-tools --git-review --installed-workflows
