# KDP Agent - Amazon Kindle Direct Publishing Automation

Zero-cost AI agent for generating and publishing Amazon KDP books. This project helps you publish 3 books per week across 7 categories with trending, high-demand content.

## Features

- **Trend Research**: Identifies trending, low-competition book ideas
- **Content Generation**: Creates 48-page interior layouts for puzzles, journals, and storybooks
- **Cover Creation**: Generates KDP-compliant 8.5" × 8.5" covers with proper spine width
- **Character Consistency**: Uses recurring themed characters across all pages

## Category Focus

1. Kids' Storytellers (ages 0-12)
2. Word Search Puzzles (ages 3-12)
3. Sudoku Puzzles (ages 6+)
4. Gratitude Journals (ages 6+)
5. Health Guides (ages 6+)
6. Story Starters (ages 6+)
7. Adult Mandalas

## Requirements

- **Python 3.8+**
- No cloud costs - runs locally on your machine

## Installation

```bash
cd kdp-agent

# Create virtual environment (optional but recommended)
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Step 1: Generate trending book ideas
python src/main.py research

# Step 2: List available ideas
python src/main.py list

# Step 3: Generate a complete book package
python src/main.py generate --id 1
python src/main.py generate --id 2
python src/main.py generate --id 3
```

## Output

Each book generates:
- `output/pdfs/{book_name}_interior.pdf` - 48-page interior
- `output/pdfs/{book_name}_cover.pdf` - Full 3-panel cover (front + spine + back)
- `output/{book_name}.zip` - Combined package for download

## Project Structure

```
kdp-agent/
├── config/
│   └── products.json      # Category definitions and KDP specs
├── src/
│   ├── main.py            # CLI interface
│   ├── research.py        # Trend analysis engine
│   ├── layout.py          # PDF generation engine
│   └── trending_keywords.txt  # Keyword database
├── output/                # Generated books and PDFs
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## KDP Publishing Workflow

1. Download the ZIP file from `output/`
2. Extract and verify PDFs
3. Log into [KDP](https://kdp.amazon.com/)
4. Click "Create a New Book"
5. Upload interior PDF → Upload cover PDF
6. Fill in title, categories, keywords from the research suggestions
7. Publish!

## Pricing Strategy

Generated books typically sell for **$5.99 - $7.99**, which gives:
- 35-60% royalty (depending on price)
- $2.10 - $4.80 per sale

## How Trends Are Determined

The research module uses:
- Google Trends data (seasonal patterns)
- Amazon bestseller keywords
- KDP Rocket competitor analysis
- Competition-to-demand ratio scoring

## Character System

Each book gets a unique, memorable character:
- Kids' books: Animal protagonists (Finley the Fish, Luna the Cat)
- Health guides: Friendly experts (Hugo the Chef)
- Journals: Personified concepts (Sunny the Sun)

Illustration style is described in placeholders for later insertion with stock images or AI art.

## GitHub Actions (Optional)

To run on GitHub instead of locally, add `.github/workflows/kdp-book-builder.yml`:

```yaml
name: Generate KDP Book
on:
  workflow_dispatch:
    inputs:
      book_id:
        description: 'Book ID to generate'
        required: true
        default: '1'
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python src/main.py generate --id ${{ github.event.inputs.book_id }}
      - uses: actions/upload-artifact@v4
        with:
          name: book-package
          path: output/*.zip
```

## License

Free for personal use. Not intended for commercial resale as a product.

## Next Steps

1. Install Python 3.8+
2. Run `python src/main.py research`
3. Review trend ideas
4. Start generating books weekly!