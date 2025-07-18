SHELL := /bin/bash


.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: ## Build the themes
	@poetry run python scripts/build.py

.PHONY: publish
publish: build ## Publish the package
	@npm run package
	@npm run publish

.PHONY: install
install: ## Install dependency
	@poetry install --no-root
	@npm install --global @vscode/vsce

hotfix: ##Upgrade of hotfix version
	@poetry run python scripts/version.py hotfix
	@poetry run python scripts/build.py

minor: ##Upgrade of minor version
	@poetry run python scripts/version.py minor
	@poetry run python scripts/build.py

major: ##Upgrade of major version
	@poetry run python scripts/version.py major
	@poetry run python scripts/build.py
