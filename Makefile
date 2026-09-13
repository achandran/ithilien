.DEFAULT_GOAL := help

UV ?= uv

# Optional checkout-local toolchain setting, never committed.
-include evaluation/local.mk

# Optional rustup installation with cargo/ and rustup/ beneath this directory.
# Otherwise use the user's normal toolchain from PATH.
RUST_RUNTIME ?=
ifneq ($(strip $(RUST_RUNTIME)),)
export CARGO_HOME := $(abspath $(RUST_RUNTIME))/cargo
export RUSTUP_HOME := $(abspath $(RUST_RUNTIME))/rustup
export PATH := $(CARGO_HOME)/bin:$(PATH)
endif

.PHONY: help test build evaluate evaluate-ghostty

# Show commands without installing dependencies or running evaluations.
help:
	@printf '%s\n' \
	  'Ithilien development' \
	  '' \
	  '  make build     Build all ports, palette assets, and the Neovim preview' \
	  '  make test      Run the normal unit and regression tests' \
	  '  make evaluate  Run tests and headless renderer/workflow evaluation' \
	  '  make evaluate-headless  Run renderer/workflow checks without GUI capture' \
	  '  make evaluate-offline   Run tests and recheck saved Ghostty screenshots' \
	  '' \
	  'Bare make shows this help. Setup and targeted diagnostics: docs/development.md'


# Run Python unit and regression tests with the locked development environment.
test:
	$(UV) run --locked pytest

# Audit both palettes, regenerate every theme port, and refresh the Neovim preview.
build:
	$(UV) run --locked python scripts/build.py

# Headless evaluation by default; add GHOSTTY_ARGS=--ghostty-capture explicitly; see docs/development.md for one-time prerequisites.
EVALUATE_OUTPUT ?= evaluation/results/full
CODEX_SOURCE ?= evaluation/deps/codex
PYTHON_SOURCE ?= evaluation/deps/tree-sitter-python
THEMES ?= ithilien-dawn
GHOSTTY_ARGS ?=

evaluate: test
	$(UV) run --locked python -m tintprobe --project-root . suite --fresh-run --strict-gates \
		--codex-source "$(CODEX_SOURCE)" --python-source "$(PYTHON_SOURCE)" \
		--output "$(EVALUATE_OUTPUT)" --themes $(THEMES) \
		--pickers --python-tools --git-review --installed-workflows $(GHOSTTY_ARGS)

# Safe while the desktop is in use: no Ghostty launch, focus, or mouse input.
# This does not certify native pixels or complete native target coverage.
.PHONY: evaluate-headless evaluate-offline
evaluate-headless:
	$(MAKE) evaluate GHOSTTY_ARGS=

evaluate-offline: test evaluate-ghostty-images

# Live Neovim cases require Neovim/Kanso; targeted --cases can isolate terminal checks.
# Native execution requires authorized Ghostty access and Screen Recording.
GHOSTTY_OUTPUT ?= evaluation/results/ghostty
GHOSTTY_CAPTURE ?= --capture
evaluate-ghostty:
	$(UV) run --locked python -m tintprobe --project-root . ghostty $(GHOSTTY_CAPTURE) --output "$(GHOSTTY_OUTPUT)"

# Analyze existing PNGs without opening or controlling Ghostty.
.PHONY: evaluate-ghostty-images
evaluate-ghostty-images:
	$(UV) run --locked python -m tintprobe --project-root . images --output "$(GHOSTTY_OUTPUT)"

.PHONY: evaluate-codex-ui
CODEX_UI_OUTPUT ?= evaluation/results/codex-ui
CODEX_UI_ARGS ?=
evaluate-codex-ui:
	$(UV) run --locked python -m tintprobe --project-root . codex-ui --source "$(CODEX_SOURCE)" --output "$(CODEX_UI_OUTPUT)" $(CODEX_UI_ARGS)

# One-time source setup; subsequent builds/evaluations do not fetch or reset repos.
.PHONY: setup-evaluation
setup-evaluation:
	$(UV) run --locked python -m tintprobe --project-root . prepare --fetch --themes $(THEMES)
