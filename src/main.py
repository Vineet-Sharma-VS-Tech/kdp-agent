#!/usr/bin/env python3
"""
Main CLI interface for KDP Agent
Usage:
    python main.py research           # Regenerate trending ideas
    python main.py generate --id 1    # Generate book with ID 1
    python main.py list               # List available ideas
"""
import argparse
import json
import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from research import KDPResearcher
from layout import (
    create_interior_pdf, create_book_cover,
    generate_word_search_puzzle, PAGE_WIDTH, PAGE_HEIGHT
)
from reportlab.lib.pagesizes import inch

PAGE_WIDTH = 8.5 * inch
PAGE_HEIGHT = 8.5 * inch
MARGIN = 0.25 * inch

def ensure_output_dirs():
    """Create output directories if they don't exist"""
    os.makedirs("output", exist_ok=True)
    os.makedirs("output/pdfs", exist_ok=True)

def cmd_research():
    """Regenerate trending ideas"""
    print("🔍 Running KDP trend research...")
    researcher = KDPResearcher(data_dir="src")
    trends = researcher.update_ideas_file()
    print(f"\n✅ Generated {len(trends)} top trending ideas:")
    for i, t in enumerate(trends[:5], 1):
        print(f"   {i}. {t['title']} - ${t['estimated_price']}")
    print(f"\n   Full list saved to: src/trending_ideas.json")

def cmd_list(category=None):
    """List available book ideas"""
    ideas_file = "src/trending_ideas.json"
    if not os.path.exists(ideas_file):
        print("❌ No ideas found. Run 'python main.py research' first.")
        return

    with open(ideas_file) as f:
        data = json.load(f)

    print(f"\n📚 Available Book Ideas (generated: {data.get('generated_at', 'unknown')})")
    print("=" * 60)

    for idea in data.get('top_trends', []):
        if category and idea['category'] != category:
            continue
        char_info = f" [{idea['character']}]" if idea.get('character') else ""
        print(f"\nID: {idea['id']}")
        print(f"   Title: {idea['title']}{char_info}")
        print(f"   Category: {idea['category']}")
        print(f"   Age Group: {idea['age_group']}")
        print(f"   Keyword: {idea['keyword']}")
        print(f"   Price: {idea['estimated_price']}")

def cmd_generate(idea_id: int):
    """Generate a complete book package"""
    ideas_file = "src/trending_ideas.json"
    if not os.path.exists(ideas_file):
        print("❌ No ideas found. Run 'python main.py research' first.")
        return

    with open(ideas_file) as f:
        data = json.load(f)

    # Find the idea
    idea = None
    for t in data.get('top_trends', []):
        if t.get('id') == idea_id:
            idea = t
            break

    if not idea:
        print(f"❌ Idea with ID {idea_id} not found.")
        print("Run 'python main.py list' to see available ideas.")
        return

    print(f"📖 Generating book: {idea['title']}")
    ensure_output_dirs()

    # Generate interior pages (48 pages total as requested)
    pages = []
    for page_num in range(1, 49):
        if page_num == 1:
            pages.append({
                'page_type': 'title',
                'content': idea['title'],
                'character': idea.get('character')
            })
        else:
            pages.append({
                'page_type': 'content',
                'content': f"Page {page_num}\n\n[Illustration space for: {idea.get('character', 'Character')}]\n\n[Content for age group {idea['age_group']}]",
                'character': idea.get('character')
            })

    # Create interior PDF
    import re
    filename = re.sub(r'[^a-zA-Z0-9_]', '_', idea['title'])
    interior_path = f"output/pdfs/{filename}_interior.pdf"
    cover_path = f"output/pdfs/{filename}_cover.pdf"

    author = "Created by AI Agent"
    create_interior_pdf(interior_path, idea['title'], author, pages, idea['category'], idea['age_group'], idea.get('character'))
    print(f"   ✅ Interior PDF: {interior_path}")

    # Create cover
    create_book_cover(cover_path, idea['title'], idea.get('character'), idea['category'], 48)
    print(f"   ✅ Cover PDF: {cover_path}")

    print(f"\n✅ Book package ready!")
    print(f"   📁 Output: output/pdfs/{filename}_interior.pdf")
    print(f"   📁 Output: output/pdfs/{filename}_cover.pdf")

    # Create ZIP for download
    import zipfile
    zip_path = f"output/{filename}.zip"
    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.write(interior_path)
        zf.write(cover_path)
    print(f"   📦 ZIP archive: {zip_path}")

def cmd_generate_puzzle(puzzle_type: str):
    """Generate a puzzle book sample"""
    print(f"🧩 Generating {puzzle_type} puzzle book sample...")
    ensure_output_dirs()

    # Sample word search
    words = ['OCEAN', 'FISH', 'WHALE', 'DOLPHIN', 'TURTLE']
    grid = generate_word_search_puzzle('OCEAN', 15)

    from io import StringIO
    from reportlab.pdfgen import canvas

    c = canvas.Canvas(f"output/pdfs/{puzzle_type}_sample.pdf", pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    c.setFont("Helvetica", 10)
    y_pos = PAGE_HEIGHT - MARGIN
    for row in grid:
        c.drawString(MARGIN, y_pos, ' '.join(row))
        y_pos -= 0.25 * inch
    c.save()
    print(f"   ✅ Sample saved: output/pdfs/{puzzle_type}_sample.pdf")

def main():
    parser = argparse.ArgumentParser(description='KDP Agent - Generate Amazon KDP Books')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Research command
    research_parser = subparsers.add_parser('research', help='Regenerate trending book ideas')

    # List command
    list_parser = subparsers.add_parser('list', help='List available book ideas')
    list_parser.add_argument('--category', type=str, help='Filter by category')

    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate a complete book package')
    generate_parser.add_argument('--id', type=int, required=True, help='Book ID from list')

    args = parser.parse_args()

    if args.command == 'research':
        cmd_research()
    elif args.command == 'list':
        cmd_list(args.category)
    elif args.command == 'generate':
        cmd_generate(args.id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()