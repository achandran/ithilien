.DEFAULT_GOAL := help

UV ?= uv

# Optional checkout-local toolchain setting, never committed.
-include tests/evaluation/local.mk

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
	  '  make evaluate  Run tests, Neovim workflows, and saved Codex checks' \
	  '  make evaluate-headless  Run renderer/workflow checks without GUI capture' \
	  '  make evaluate-full      Opt-in source-built Codex suite (large Rust cache)' \
	  '  make evaluate-offline   Run tests and recheck saved Ghostty screenshots' \
	  '' \
	  'Bare make shows this help. Setup and targeted diagnostics: docs/development.md'


# Run Python unit and regression tests with the locked development environment.
test:
	$(UV) run --locked pytest

# Audit the Dawn palette, regenerate every theme port, and refresh the Neovim preview.
build:
	$(UV) run --locked python scripts/build.py

# Routine evaluation uses saved Codex evidence; full source replay is opt-in.
EVALUATE_OUTPUT ?= tests/evaluation/results/routine
CODEX_SOURCE ?= tests/evaluation/deps/codex
PYTHON_SOURCE ?= tests/evaluation/deps/tree-sitter-python
THEMES ?= ithilien-dawn
GHOSTTY_ARGS ?=

# Routine checks never compile Codex or create per-run Swift caches.
evaluate: test
	$(UV) run --locked python -m tintprobe --project-root . compare --strict-gates --python-source "$(PYTHON_SOURCE)" --output "$(EVALUATE_OUTPUT)/neovim" --themes $(THEMES)
	$(UV) run --locked python -m tintprobe --project-root . workflow evaluate_pickers --output "$(EVALUATE_OUTPUT)/pickers"
	$(UV) run --locked python -m tintprobe --project-root . workflow evaluate_python_tools --output "$(EVALUATE_OUTPUT)/python-tools"
	$(UV) run --locked python -m tintprobe --project-root . workflow evaluate_git_review --output "$(EVALUATE_OUTPUT)/git-review"
	$(UV) run --locked python -m tintprobe --project-root . workflow evaluate_installed_workflows --output "$(EVALUATE_OUTPUT)/installed-workflows"
	$(MAKE) evaluate-codex-recording

.PHONY: evaluate-full evaluate-codex-recording
CODEX_RECORDING ?= tests/evaluation/results/codex-recording/codex-cells.json
evaluate-codex-recording:
	$(UV) run --locked python scripts/check_codex_recording.py --recording "$(CODEX_RECORDING)" --output "$(EVALUATE_OUTPUT)/codex-recording.json"

# Opt-in deep check. Keep its rebuildable output outside this checkout.
export CARGO_TARGET_DIR ?= $(HOME)/Library/Caches/ithilien/codex-target
export CARGO_PROFILE_DEV_DEBUG ?= 0
export CARGO_PROFILE_TEST_DEBUG ?= 0
export CARGO_INCREMENTAL ?= 0
FULL_OUTPUT ?= tests/evaluation/results/full
evaluate-full: test
	$(UV) run --locked python -m tintprobe --project-root . suite --fresh-run --strict-gates \
		--codex-source "$(CODEX_SOURCE)" --python-source "$(PYTHON_SOURCE)" \
		--output "$(FULL_OUTPUT)" --themes $(THEMES) \
		--pickers --python-tools --git-review --installed-workflows $(GHOSTTY_ARGS)

# Safe while the desktop is in use: no Ghostty launch, focus, or mouse input.
# This does not certify native pixels or complete native target coverage.
.PHONY: evaluate-headless evaluate-offline
evaluate-headless:
	$(MAKE) evaluate GHOSTTY_ARGS=

evaluate-offline: test evaluate-ghostty-images

# Live Neovim cases require Neovim/Kanso; targeted --cases can isolate terminal checks.
# Native execution requires authorized Ghostty access and Screen Recording.
GHOSTTY_OUTPUT ?= tests/evaluation/results/ghostty
GHOSTTY_CAPTURE ?= --capture
evaluate-ghostty:
	$(UV) run --locked python -m tintprobe --project-root . ghostty $(GHOSTTY_CAPTURE) --output "$(GHOSTTY_OUTPUT)"

# Analyze existing PNGs without opening or controlling Ghostty.
.PHONY: evaluate-ghostty-images
evaluate-ghostty-images:
	$(UV) run --locked python -m tintprobe --project-root . images --output "$(GHOSTTY_OUTPUT)"

.PHONY: evaluate-codex-ui
CODEX_UI_OUTPUT ?= tests/evaluation/results/codex-ui
CODEX_UI_ARGS ?=
evaluate-codex-ui:
	$(UV) run --locked python -m tintprobe --project-root . codex-ui --source "$(CODEX_SOURCE)" --output "$(CODEX_UI_OUTPUT)" $(CODEX_UI_ARGS)

# One-time source setup; subsequent builds/evaluations do not fetch or reset repos.
.PHONY: setup-evaluation
setup-evaluation:
	$(UV) run --locked python -m tintprobe --project-root . prepare --fetch --themes $(THEMES)
