# LeakIXClient-Python Makefile

.PHONY: help
help: ## Ask for help!
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; \
		{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install dependencies
	poetry install

.PHONY: build
build: ## Build the package
	poetry build

.PHONY: test
test: ## Run tests
	poetry run pytest

.PHONY: test-cov
test-cov: ## Run tests with coverage
	poetry run pytest --cov=leakix --cov-report=term-missing

.PHONY: format
format: ## Format code with ruff
	poetry run ruff format leakix/ tests/ example/ executable/

.PHONY: check-format
check-format: ## Check code formatting
	poetry run ruff format --check leakix/ tests/ example/ executable/

.PHONY: lint
lint: ## Run ruff linter
	poetry run ruff check leakix/ tests/ example/ executable/

.PHONY: lint-fix
lint-fix: ## Run ruff linter with auto-fix
	poetry run ruff check --fix leakix/ tests/ example/ executable/

.PHONY: typecheck
typecheck: ## Run mypy type checker
	poetry run mypy leakix/

.PHONY: audit
audit: ## Run security audit
	poetry run pip-audit

.PHONY: check
check: check-format lint typecheck test ## Run all checks

.PHONY: check-outdated
check-outdated: ## Check for outdated dependencies
	poetry show --outdated || true

.PHONY: lint-shell
lint-shell: ## Lint shell scripts using shellcheck
	shellcheck .github/scripts/*.sh

.PHONY: clean
clean: ## Clean build artifacts
	rm -rf dist/ build/ *.egg-info/ .pytest_cache/ .mypy_cache/ .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Trailing whitespace targets
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    SED := $(shell command -v gsed 2>/dev/null)
    ifeq ($(SED),)
        $(error GNU sed (gsed) not found on macOS. Install with: brew install gnu-sed)
    endif
else
    SED := sed
endif

.PHONY: fix-trailing-whitespace
fix-trailing-whitespace: ## Remove trailing whitespaces from all files
	@echo "Removing trailing whitespaces from all files..."
	@find . -type f \( \
		-name "*.py" -o -name "*.toml" -o -name "*.md" -o -name "*.yaml" \
		-o -name "*.yml" -o -name "*.json" \) \
		-not -path "./.git/*" \
		-not -path "./.mypy_cache/*" \
		-not -path "./.pytest_cache/*" \
		-not -path "./.ruff_cache/*" \
		-exec sh -c \
			'$(SED) -i -e "s/[[:space:]]*$$//" "$$1"' \
			_ {} \; && \
		echo "Trailing whitespaces removed."

.PHONY: check-trailing-whitespace
check-trailing-whitespace: ## Check for trailing whitespaces in source files
	@echo "Checking for trailing whitespaces..."
	@files_with_trailing_ws=$$(find . -type f \( \
		-name "*.py" -o -name "*.toml" -o -name "*.md" -o -name "*.yaml" \
		-o -name "*.yml" -o -name "*.json" \) \
		-not -path "./.git/*" \
		-not -path "./.mypy_cache/*" \
		-not -path "./.pytest_cache/*" \
		-not -path "./.ruff_cache/*" \
		-exec grep -l '[[:space:]]$$' {} + 2>/dev/null || true); \
	if [ -n "$$files_with_trailing_ws" ]; then \
		echo "Files with trailing whitespaces found:"; \
		echo "$$files_with_trailing_ws" | sed 's/^/  /'; \
		echo ""; \
		echo "Run 'make fix-trailing-whitespace' to fix automatically."; \
		exit 1; \
	else \
		echo "No trailing whitespaces found."; \
	fi
