"""
PDF Layout and Cover Generator for KDP Books
Generates 8.5" x 8.5" paperback interiors and covers with proper margins and bleed
"""
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
import os
import math

PAGE_WIDTH = 8.5 * inch
PAGE_HEIGHT = 8.5 * inch
BLEED = 0.125 * inch
MARGIN = 0.25 * inch

def calculate_spine_width(page_count, paper_type='white', gsm=80):
    """
    Calculate spine width for KDP paperbacks
    KDP formula: (page_count / 2) * 0.002252 for white paper, 80gsm
    """
    if paper_type.lower() == 'cream':
        thickness = page_count * 0.00238
    else:  # white paper
        thickness = page_count * 0.00225
    return thickness * inch

def generate_sudoku_grid(difficulty='easy'):
    """Generate a simple Sudoku grid (partial for sample)"""
    import random
    grid = [[0 for _ in range(9)] for _ in range(9)]
    # Very basic: fill some numbers
    for i in range(15 if difficulty == 'easy' else 10):
        r, c = random.randint(0, 8), random.randint(0, 8)
        grid[r][c] = random.randint(1, 9)
    return grid

def create_interior_pdf(filepath, title, author, pages_content, category, age_group, character_name=None):
    """
    Create interior PDF for 8.5" x 8.5" book
    """
    c = canvas.Canvas(filepath, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    for i, page in enumerate(pages_content):
        page_num = i + 1

        if page['page_type'] == 'title':
            c.setFont("Helvetica-Bold", 36)
            y = PAGE_HEIGHT - 2*inch
            for line in title.split(':'):
                c.drawCentredString(PAGE_WIDTH/2, y, line.strip())
                y -= 0.5*inch

            c.setFont("Helvetica", 18)
            c.drawCentredString(PAGE_WIDTH/2, 2*inch, f"A {category.replace('_', ' ').title()}")
            if character_name:
                c.drawCentredString(PAGE_WIDTH/2, 1.5*inch, f"Featuring {character_name}")

        else:
            # Draw header
            c.setFont("Helvetica-Bold", 14)
            c.drawString(MARGIN, PAGE_HEIGHT - MARGIN, title[:40] + "..." if len(title) > 40 else title)

            y = PAGE_HEIGHT - MARGIN - 0.5*inch

            if category == 'kids_storytellers':
                c.setFont("Helvetica", 12)
                story_lines = [
                    f"Chapter {page_num - 1}",
                    "",
                    f"Once upon a time, {character_name} was exploring the candy kingdom.",
                    "The gumdrop trees were shimmering in the sunlight.",
                    f"'{character_name.split()[0]}!' called a friendly marshmallow bird.",
                    "There was a mysterious path made of chocolate bars leading deep into the woods.",
                    "",
                    "[Illustration space for consistent character poses]"
                ]
                for line in story_lines:
                    c.drawString(MARGIN, y, line)
                    y -= 0.2*inch

            elif category == 'word_search_kids':
                c.setFont("Courier-Bold", 14)
                c.drawString(MARGIN, y, "FIND THE HIDDEN WORDS!")
                y -= 0.4*inch
                words = ["FISH", "OCEAN", "MAGIC", "BRAVE", "LUNA", "PIXIE"]
                grid = generate_word_search_puzzle(random.choice(words), 12)
                for row in grid:
                    c.drawCentredString(PAGE_WIDTH/2, y, "  ".join(row))
                    y -= 0.25*inch
                y -= 0.5*inch
                c.setFont("Helvetica-Bold", 10)
                c.drawString(MARGIN, y, "WORDS TO FIND: " + ", ".join(words))

            elif category == 'sudoku_puzzles':
                c.setFont("Helvetica-Bold", 18)
                c.drawCentredString(PAGE_WIDTH/2, y, f"Sudoku Puzzle #{page_num - 1}")
                y -= 0.5*inch
                grid = generate_sudoku_grid()
                cell_size = 0.4*inch
                start_x = (PAGE_WIDTH - 9*cell_size)/2
                for r in range(10):
                    c.line(start_x, y - r*cell_size, start_x + 9*cell_size, y - r*cell_size)
                    c.line(start_x + r*cell_size, y, start_x + r*cell_size, y - 9*cell_size)

                c.setFont("Helvetica-Bold", 14)
                for r in range(9):
                    for col in range(9):
                        val = grid[r][col]
                        if val != 0:
                            c.drawCentredString(start_x + col*cell_size + cell_size/2, y - r*cell_size - cell_size + 5, str(val))

            else:
                c.setFont("Helvetica", 12)
                c.drawString(MARGIN, y, f"Welcome to page {page_num} of your {category.replace('_', ' ')}!")
                c.drawString(MARGIN, y - 0.3*inch, "Write your thoughts and feelings here...")
                c.line(MARGIN, y - 0.6*inch, PAGE_WIDTH - MARGIN, y - 0.6*inch)
                c.line(MARGIN, y - 1.0*inch, PAGE_WIDTH - MARGIN, y - 1.0*inch)
                c.line(MARGIN, y - 1.4*inch, PAGE_WIDTH - MARGIN, y - 1.4*inch)

            # Footer
            c.setFont("Helvetica", 8)
            c.drawCentredString(PAGE_WIDTH/2, MARGIN/2, f"Page {page_num} | Copyright (c) 2024")

        c.showPage()

    c.save()
    return filepath

def _draw_cover_page(c, page):
    """Draw a page with image placeholder for character"""
    c.setFillColor(colors.white)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)

    # Character illustration area
    c.setStrokeColor(colors.grey)
    c.rect(MARGIN, MARGIN + 2*inch, PAGE_WIDTH - 2*MARGIN, PAGE_HEIGHT - 3*MARGIN, fill=0)

    # Character name
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - MARGIN/2, page.get('character', 'Character'))

def _add_back_cover(c, title, character_name=None):
    """Add back cover with ISBN placeholder and character"""
    c.setFillColor(colors.white)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)

    c.setFont("Helvetica", 12)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2, f"\"{title}\"")
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 - 0.5*inch, "Amazon Kindle Direct Publishing")

    if character_name:
        c.setFont("Helvetica-Oblique", 10)
        c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT/2 - 1*inch, f"Illustrated by {character_name}")

def create_book_cover(filepath, title, character_name, category, page_count):
    """
    Create full wrap-around cover PDF for KDP
    Dimensions: (width + 2*bleed) x (height + 2*bleed) for front + bleed
    Plus back cover and spine
    """
    spine_width = calculate_spine_width(page_count)
    total_width = PAGE_WIDTH + 2*BLEED + spine_width + 2*BLEED
    total_height = PAGE_HEIGHT + 2*BLEED

    c = canvas.Canvas(filepath, pagesize=(total_width, total_height))

    # Draw front cover
    front_x = 2*BLEED
    _draw_single_cover(c, title, character_name, category, front_x, 0, PAGE_WIDTH, PAGE_HEIGHT)

    # Draw spine
    spine_x = front_x + PAGE_WIDTH + 2*BLEED
    c.setFillColor(colors.lightgrey)
    c.rect(spine_x, BLEED, spine_width, PAGE_HEIGHT, fill=1)

    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(spine_x + spine_width/2, PAGE_HEIGHT/2, "CHILDREN'S BOOK")

    # Draw back cover
    back_x = front_x + PAGE_WIDTH + 4*BLEED + spine_width
    _draw_single_cover(c, f"{title}\n\nA Story by...", character_name, category, back_x, 0, PAGE_WIDTH, PAGE_HEIGHT, is_back=True)

    c.save()

def _draw_single_cover(c, title, character_name, category, x, y, width, height, is_back=False):
    """Draw a single cover section"""
    c.saveState()
    c.translate(x, y)

    # Background
    if is_back:
        c.setFillColorRGB(0.95, 0.95, 0.98)
        c.rect(0, 0, width, height, fill=1)
    else:
        c.setFillColorRGB(1, 1, 1)
        c.rect(0, 0, width, height, fill=1)

    # Title
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 24 if not is_back else 14)

    if is_back:
        c.drawCentredString(width/2, height - 0.5*inch, title[:40] if len(title) > 40 else title)
        c.setFont("Helvetica", 10)
        c.drawCentredString(width/2, height - 1.5*inch, "A Story by...")
    else:
        lines = []
        words = title.split()
        current_line = []
        for word in words:
            if current_line and len(' '.join(current_line + [word])) > 6:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                current_line.append(word)
        if current_line:
            lines.append(' '.join(current_line))

        y_pos = height - 1.5*inch
        for line in lines:
            c.drawCentredString(width/2, y_pos, line)
            y_pos -= 0.4*inch

        # Character name
        c.setFont("Helvetica", 12)
        c.drawCentredString(width/2, height/4, f"by {character_name}")

    c.restoreState()

def generate_word_search_puzzle(word, size=15):
    """Generate a word search grid containing the word"""
    import random
    grid = [[' ' for _ in range(size)] for _ in range(size)]

    # Place the word horizontally
    row = random.randint(0, size-1)
    col = random.randint(0, size-len(word))
    for i, char in enumerate(word):
        grid[row][col+i] = char.upper()

    # Fill remaining with random letters
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for r in range(size):
        for c in range(size):
            if grid[r][c] == ' ':
                grid[r][c] = random.choice(letters)

    return grid

if __name__ == "__main__":
    # Test cover generation
    test_ideas = [
        {"title": "Ocean Adventures of Finley the Fish", "character": "Finley the Fish"},
        {"title": "Healthy Habits with Chef Hero Hugo", "character": "Hugo the Friendly Chef"},
    ]

    for idea in test_ideas:
        cover_path = f"output/{idea['title'].replace(' ', '_')}_cover.pdf"
        create_book_cover(cover_path, idea['title'], idea['character'], "kids_storytellers", 48)
        print(f"Generated: {cover_path}")