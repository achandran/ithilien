.DEFAULT_GOAL := help
UV ?= uv

.PHONY: help test build check-neovim

help:
	@printf '%s\n' 'Ithilien development' '' \
	  '  make build          Audit palettes and regenerate ports and README assets' \
	  '  make test           Run unit and regression tests' \
	  '  make check-neovim   Run native highlight, contrast, diff, and plugin checks'

test:
	$(UV) run --locked pytest

build:
	$(UV) run --locked python scripts/build.py

check-neovim:
	nvim --headless -u NONE -i NONE -l tests/check_highlights.lua
	$(UV) run --locked python tests/check_highlight_contrast.py
	nvim --headless -u NONE -i NONE -l tests/check_dusk.lua
	nvim --headless -u NONE -i NONE -l tests/check_native_diff.lua
	nvim --headless -u NONE -i NONE -l tests/check_diff_presentation.lua
	nvim --headless -u NONE -i NONE -l tests/check_plugin_semantics.lua
