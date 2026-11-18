.PHONY: help install research list generate clean

## Default target
help:
	@echo "KDP Agent - Build and run commands"
	@echo ""
	@echo "Usage:"
	@echo "  make install    - Install dependencies"
	@echo "  make research   - Generate trending book ideas"
	@echo "  make list       - Show available book ideas"
	@echo "  make generate   - Generate a book (requires BOOK_ID)"
	@echo "  make clean        - Clean generated files"
	@echo ""
	@echo "Examples:"
	@echo "  make install"
	@echo "  make research"
	@echo "  make generate BOOK_ID=1"

## Install dependencies
install:
	pip install -r requirements.txt

## Run trend research
research:
	python src/main.py research

## List book ideas
list:
	python src/main.py list

## Generate a book
generate:
ifndef BOOK_ID
	@echo "Error: BOOK_ID is required"
	@echo "Usage: make generate BOOK_ID=1"
	@exit 1
endif
	python src/main.py generate --id $(BOOK_ID)

## Clean output files
clean:
	rm -rf output/*.zip
	rm -rf output/pdfs/*.pdf