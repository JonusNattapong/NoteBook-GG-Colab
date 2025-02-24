import json
import os
from datetime import datetime

def load_notebooks():
    """Load notebooks data from JSON file"""
    with open('data/notebooks.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_readme_content(data):
    """Generate README content with notebook information"""
    content = ["# NoteBook-GG-Colab\n"]
    content.append("Collection of Google Colab Notebooks for various topics.\n")
    
    # Add notebooks table
    content.append("## Available Notebooks\n")
    content.append("| Title | Category | Description | Last Updated | Colab Link |")
    content.append("|-------|----------|-------------|--------------|------------|")
    
    for notebook in data['notebooks']:
        # Create Colab badge
        colab_badge = f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({notebook['colabLink']})"
        
        # Add row to table
        row = [
            notebook['title'],
            notebook['category'],
            notebook['description'],
            notebook['lastUpdated'],
            colab_badge
        ]
        content.append(f"| {' | '.join(row)} |")
    
    # Add categories section
    categories = {}
    for notebook in data['notebooks']:
        cat = notebook['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(notebook)
    
    content.append("\n## Categories\n")
    for category, notebooks in sorted(categories.items()):
        content.append(f"\n### {category}")
        for notebook in notebooks:
            content.append(f"- {notebook['title']}")
            content.append(f"  - Tags: {', '.join(notebook['tags'])}")
    
    # Add footer
    content.append("\n---")
    content.append(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return "\n".join(content)

def update_readme():
    """Update README.md with current notebook information"""
    try:
        # Load data
        data = load_notebooks()
        
        # Generate new content
        new_content = generate_readme_content(data)
        
        # Write to README
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print("README.md has been successfully updated!")
        
    except Exception as e:
        print(f"Error updating README: {str(e)}")

if __name__ == "__main__":
    update_readme()
