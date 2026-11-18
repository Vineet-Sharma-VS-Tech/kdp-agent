"""
Research module for KDP Agent
Analyzes trending data and generates book ideas based on low competition, high demand
"""
import json
import os
import random
from datetime import datetime
from typing import List, Dict, Optional

class KDPResearcher:
    def __init__(self, data_dir: str = "src"):
        self.data_dir = data_dir
        self.trending_file = os.path.join(data_dir, "trending_keywords.txt")
        self.ideas_file = os.path.join(data_dir, "trending_ideas.json")
        self.categories_file = "config/products.json"

    def load_trending_keywords(self) -> List[Dict]:
        """Load trending keywords from data file"""
        keywords = []
        with open(self.trending_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('|')
                    if len(parts) >= 5:
                        keywords.append({
                            'category': parts[0],
                            'keyword': parts[1],
                            'age_group': parts[2],
                            'competition': parts[3],
                            'demand': parts[4]
                        })
        return keywords

    def load_existing_ideas(self) -> Dict:
        """Load existing trend ideas"""
        if os.path.exists(self.ideas_file):
            with open(self.ideas_file, 'r') as f:
                return json.load(f)
        return {"trending_ideas": [], "top_trends": []}

    def generate_idea(self, keyword_data: Dict, existing_titles: set) -> Dict:
        """Generate a book idea from keyword data"""
        # Character templates by category
        character_templates = {
            'kids_storytellers': [
                ('The Adventures of {character}: A Magical {theme} Tale', {'character': ['Finley the Fish', 'Leo the Lion', 'Mila the Mouse', 'Noah the Narwhal'],
                                                                                         'theme': ['Ocean', 'Forest', 'Space', 'Candy Kingdom', 'Farm', 'Castle']}),
                ('{character} and the {adjective} Quest', {'character': ['Pip the Penguin', 'Ruby the Rabbit', 'Sam the Squirrel', 'Tilly the Turtle'],
                                                           'adjective': ['Brave', 'Curious', 'Swift', 'Bright', 'Gentle']}),
                ('{character} Goes on a {adjective} Adventure', {'character': ['Ollie the Octopus', 'Wally the Whale', 'Zara the Zebra', 'Barnaby the Bear'],
                                                                 'adjective': ['Magical', 'Wonderful', 'Amazing', 'Mysterious', 'Grand']}),
            ],
            'word_search_kids': [
                ('{theme} Word Search for {age}', {'theme': ['Animal', 'Ocean', 'Dinosaur', 'Space', 'Farm', 'Jungle', 'Weather', 'Colors', 'Shapes', 'Transportation']}),
            ],
            'sudoku_puzzles': [
                ('Easy Sudoku for {age}', {'age': ['Kids', 'Teens', 'Seniors']}),
            ],
            'gratitude_journal': [
                ('{greeting} Gratitude Journal for {age}', {'greeting': ['Morning', 'Daily', 'Sunny', 'Happy', 'Joyful', 'Thankful', 'Peaceful', 'Blessed']}),
            ],
            'health_guide': [
                ('Healthy Habits with {character}', {'character': ['Chef Hugo', 'Fit Fred', 'Dr. Daisy', 'Mr. Munch', 'Nurse Nina', 'Coach Carl', 'Dr. Emma']}),
            ],
            'story_starters': [
                ('{adjective} Story Starters for {age}', {'adjective': ['Magic', 'Wonderful', 'Brave', 'Curious', 'Colorful', 'Creative', 'Imaginative', 'Mysterious']}),
            ],
            'mandalas_adult': [
                ('{theme} Mandalas for Relaxation', {'theme': ['Ocean', 'Flowers', 'Geometric', 'Nature', 'Abstract', 'Zen', 'Spiral', 'Colorful']}),
            ]
        }

        # Generate title
        templates = character_templates.get(keyword_data['category'], [['{keyword} Book']])
        template = random.choice(templates)  # Pick random template for variety

        # Fill in placeholders
        title = template[0]
        placeholders = template[1] if len(template) > 1 else {}

        for key, values in placeholders.items():
            if key in title:
                choices = values if isinstance(values, list) else [values]
                title = title.replace(f'{{{key}}}', random.choice(choices) if choices else key)
            else:
                title = title.replace(f'{{{key}}}', 'Special')

        # Make unique
        base_title = title
        counter = 1
        while title in existing_titles:
            title = f"{base_title} Volume {counter}"
            counter += 1

        # Generate character name (one character per book, unique per book)
        character = None
        if keyword_data['category'] != 'word_search_kids':
            character_map = {
                'kids_storytellers': [
                    'Finley the Fish', 'Leo the Lion', 'Mila the Mouse', 'Noah the Narwhal',
                    'Nova the Nightingale', 'Ollie the Octopus', 'Pip the Penguin', 'Ruby the Rabbit',
                    'Sam the Squirrel', 'Tilly the Turtle', 'Wally the Whale', 'Zara the Zebra',
                    'Barnaby the Bear', 'Dexter the Dragon', 'Ella the Elephant', 'Finn the Fox'
                ],
                'health_guide': [
                    'Hugo the Friendly Chef', 'Fit Fred the Fox', 'Dr. Daisy the Dog',
                    'Mr. Munch the Mouse', 'Nurse Nina the Narwhal', 'Coach Carl the Cat',
                    'Dr. Emma the Elephant', 'Gym Gus the Gorilla', 'Wellness Wendy the Whale',
                    'Healthy Holly the Hedgehog', 'Dr. Alex the Alligator', 'Trainer Tom the Tiger'
                ],
                'gratitude_journal': [
                    'Sunny the Sun', 'Star the Star', 'Moon the Moonbeam', 'Rainbow the Cloud',
                    'Sparkle the Butterfly', 'Glow the Firefly', 'Hope the Dove', 'Joy the Jellyfish',
                    'Blessing the Bee', 'Gratitude the Grasshopper', 'Happiness the Hummingbird',
                    'Smile the Snail'
                ],
                'story_starters': [
                    'Luna the Cat', 'Magic Mike the Mouse', 'Brave Bella the Bear',
                    'Curious Charlie the Cat', 'Wonder Wendy the Whale', 'Imagin the Iguana',
                    'Dreamer the Dolphin', 'Explorer Ella the Elephant', 'Captain Kai the Koala',
                    'Wizard Wally the Wolf', 'Adventurer Alex the Alligator', 'Explorer Zoe the Zebra'
                ],
                'mandalas_adult': [
                    'Cloud the Calm Dragon', 'Serene the Serpent', 'Peaceful the Panda',
                    'Meditative the Moose', 'Tranquil the Tiger', 'Zen the Zebra',
                    'Still the Swan', 'Quiet the Quail', 'Gentle the Gazelle',
                    'Mindful the Monkey', 'Calm the Camel', 'Serenity the Snail'
                ]
            }
            options = character_map.get(keyword_data['category'], ['Mystery Character'])
            character = random.choice(options)

        return {
            'title': title,
            'category': keyword_data['category'],
            'age_group': keyword_data['age_group'],
            'keyword': keyword_data['keyword'],
            'character': character,
            'competition_score': keyword_data['competition'],
            'demand_score': keyword_data['demand'],
            'estimated_price': '$5.99-$7.99',
            'pages': 48,
            'reasoning': f"Keyword '{keyword_data['keyword']}' has {keyword_data['demand']} demand and {keyword_data['competition']} competition"
        }

    def run_research(self, count: int = 100) -> List[Dict]:
        """Run full research and generate ideas"""
        keywords = self.load_trending_keywords()
        existing = self.load_existing_ideas()
        existing_titles = {idea['title'] for idea in existing.get('top_trends', [])}

        ideas = []
        for kw in keywords:
            if len(ideas) >= count:
                break
            # Generate multiple ideas per keyword
            for _ in range(3):
                if len(ideas) >= count:
                    break
                idea = self.generate_idea(kw, existing_titles)
                if idea['title'] not in existing_titles:
                    idea['id'] = len(ideas) + 1
                    ideas.append(idea)
                    existing_titles.add(idea['title'])

        return ideas

    def get_top_trends(self, ideas: List[Dict], count: int = 10) -> List[Dict]:
        """Rank and filter top trending ideas"""
        # Priority: high demand + low competition
        def score(idea):
            demand = 10 if idea['demand_score'] == 'high' else 5 if idea['demand_score'] == 'medium' else 2
            competition = -5 if idea['competition_score'] == 'low' else -2 if idea['competition_score'] == 'medium' else 0
            return demand + competition

        ranked = sorted(ideas, key=score, reverse=True)
        return ranked[:count]

    def update_ideas_file(self):
        """Regenerate and save ideas file"""
        ideas = self.run_research()
        top_trends = self.get_top_trends(ideas)

        data = {
            "generated_at": datetime.now().isoformat(),
            "total_ideas": len(ideas),
            "top_trends": top_trends,
            "all_ideas": ideas
        }

        with open(self.ideas_file, 'w') as f:
            json.dump(data, f, indent=2)

        return top_trends


if __name__ == "__main__":
    researcher = KDPResearcher(data_dir="src")
    trends = researcher.update_ideas_file()
    print(f"Generated {len(trends)} top trending ideas:")
    for t in trends:
        print(f"  - {t['title']} ({t['category']})")