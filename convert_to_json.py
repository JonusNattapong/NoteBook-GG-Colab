import re
import json
import argparse
from typing import Dict, List, Optional

class NotebookConverter:
    def __init__(self):
        self.categories = ['Tools', 'Fine-tuning', 'Quantization', 'Other']
        
    def extract_tables(self, content: str) -> Dict[str, List[Dict]]:
        """Extract all tables from markdown content by category"""
        notebooks = []
        current_category = None
        
        # Split content by sections
        sections = content.split('###')
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
                
            # Get category name
            category_line = section.split('\n')[0].strip()
            if category_line in self.categories:
                current_category = category_line
                
                # Extract table
                table_lines = []
                for line in section.split('\n'):
                    if '|' in line:
                        table_lines.append(line)
                
                if table_lines:
                    # Parse table
                    headers = [h.strip() for h in table_lines[0].split('|')[1:-1]]
                    for row in table_lines[2:]:  # Skip header and separator lines
                        cells = [cell.strip() for cell in row.split('|')[1:-1]]
                        if len(cells) >= 3:  # Ensure valid row
                            notebook = {
                                'title': re.sub(r'\*\*(.*?)\*\*', r'\1', cells[0]),  # Remove bold markdown
                                'description': cells[1],
                                'category': current_category,
                                'tags': [],  # Will be filled based on description
                                'lastUpdated': "2025-01-18"
                            }
                            
                            # Extract article and notebook links based on table format
                            if len(cells) == 3:  # Tools format
                                notebook['colabLink'] = re.findall(r'\((.*?)\)', cells[2])[0]
                                notebook['articleLink'] = ""
                            else:  # Other categories format
                                notebook['articleLink'] = re.findall(r'\((.*?)\)', cells[2])[0] if 'Article' in cells[2] else ""
                                notebook['colabLink'] = re.findall(r'\((.*?)\)', cells[3])[0]
                            
                            # Generate tags from description
                            desc_lower = notebook['description'].lower()
                            if 'fine-tune' in desc_lower or 'fine-tuning' in desc_lower:
                                notebook['tags'].append('fine-tuning')
                            if 'quantiz' in desc_lower:
                                notebook['tags'].append('quantization')
                            if 'llm' in desc_lower:
                                notebook['tags'].append('llm')
                            if 'model' in desc_lower:
                                notebook['tags'].append('model')
                                
                            notebooks.append(notebook)
        
        return {'notebooks': notebooks}

    def save_json(self, data: Dict, output_file: str):
        """Save data to JSON file with proper formatting"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def convert_file(self, input_file: str, output_file: str):
        """Convert markdown file to JSON"""
        try:
            # Read markdown file
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract and parse tables
            data = self.extract_tables(content)
            
            # Save to JSON file
            self.save_json(data, output_file)
            print(f"Successfully converted {input_file} to {output_file}")
            
        except Exception as e:
            print(f"Error converting file: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Convert markdown tables to JSON format')
    parser.add_argument('input_file', help='Input markdown file')
    parser.add_argument('output_file', help='Output JSON file')
    
    args = parser.parse_args()
    
    converter = NotebookConverter()
    converter.convert_file(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
