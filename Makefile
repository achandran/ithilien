.DEFAULT_GOAL := test

UV ?= uv

.PHONY: test build

# Run Python unit and regression tests with the locked development environment.
test:
	$(UV) run --locked pytest

# Audit both palettes, regenerate every theme port, and refresh README previews.
build:
	$(UV) run --locked python scripts/build.py
