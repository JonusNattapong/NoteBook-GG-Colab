import json
import os
from datetime import datetime

def load_notebooks():
    """Load notebooks data from JSON file"""
    with open('data/notebooks.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_table(notebooks, include_article=True):
    """Generate markdown table for notebooks"""
    if include_article:
        headers = ["Notebook Name", "Description", "Article", "Notebook"]
        table = ["| " + " | ".join(headers) + " |",
                "|" + "|".join(["---" for _ in headers]) + "|"]
        
        for notebook in notebooks:
            article = f"[Article]({notebook['articleLink']})" if notebook['articleLink'] else ""
            colab = f"[Notebook]({notebook['colabLink']})"
            row = [
                f"**{notebook['title']}**",
                notebook['description'],
                article,
                colab
            ]
            table.append("| " + " | ".join(row) + " |")
    else:
        headers = ["Notebook Name", "Description", "Notebook"]
        table = ["| " + " | ".join(headers) + " |",
                "|" + "|".join(["---" for _ in headers]) + "|"]
        
        for notebook in notebooks:
            colab = f"[Notebook]({notebook['colabLink']})"
            row = [
                f"**{notebook['title']}**",
                notebook['description'],
                colab
            ]
            table.append("| " + " | ".join(row) + " |")
    
    return "\n".join(table)

def generate_readme_content(data):
    """Generate README content with notebook information"""
    content = ["# Top AI/LLM learning resource in 2025\n"]
    content.append(f"Jan {datetime.now().strftime('%d')}, {datetime.now().strftime('%Y')}\n")
    
    content.append("The Blog is organized into three main segments:\n")
    content.append("1. **LLM Fundamentals** (optional) – Covers essential topics such as mathematics, Python, and neural networks.")
    content.append("2. **The LLM Scientist** – Concentrates on creating the best-performing LLMs using state-of-the-art techniques.")
    content.append("3. **The LLM Engineer** – Focuses on building applications based on LLMs and deploying them.\n")
    
    content.append("* * *\n")
    content.append("### 📝 Notebooks\n")
    content.append("Below is a collection of notebooks and articles dedicated to LLMs.\n")
    
    # Group notebooks by category
    categories = {}
    for notebook in data['notebooks']:
        cat = notebook['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(notebook)
    
    # Tools section (without Article column)
    content.append("### Tools")
    tools_notebooks = categories.get('Tools', [])
    content.append(generate_table(tools_notebooks, include_article=False))
    content.append("")
    
    # Other categories (with Article column)
    other_categories = ['Fine-tuning', 'Quantization', 'Other']
    for category in other_categories:
        if category in categories:
            content.append(f"\n### {category}")
            content.append(generate_table(categories[category]))
            content.append("")
    
    # Add footer
    content.append("* * *")
    
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
