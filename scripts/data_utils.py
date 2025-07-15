#!/usr/bin/env python3
"""
Data processing utilities for Gov Terms AI.
This script provides utilities for data validation, cleaning, and processing.
"""

import json
import csv
import os
import re
from pathlib import Path
from typing import List, Dict, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataProcessor:
    """Utility class for processing government terms data."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def validate_term_data(self, term_data: Dict[str, Any]) -> bool:
        """Validate that term data has required fields."""
        required_fields = ['term', 'definition', 'source']
        optional_fields = ['category', 'tags', 'url', 'last_updated']
        
        # Check required fields
        for field in required_fields:
            if field not in term_data or not term_data[field]:
                logger.warning(f"Missing required field: {field}")
                return False
        
        # Validate data types
        if not isinstance(term_data['term'], str):
            logger.warning("Term must be a string")
            return False
        
        if not isinstance(term_data['definition'], str):
            logger.warning("Definition must be a string")
            return False
        
        if len(term_data['definition']) < 10:
            logger.warning("Definition too short")
            return False
        
        return True
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text data."""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove non-printable characters
        text = ''.join(char for char in text if char.isprintable() or char.isspace())
        
        # Fix common encoding issues
        replacements = {
            '"': '"',
            '"': '"',
            ''': "'",
            ''': "'",
            '–': '-',
            '—': '-',
            '…': '...'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text
    
    def load_json_data(self, filepath: str) -> List[Dict[str, Any]]:
        """Load and validate JSON data."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                logger.error("JSON data must be a list of objects")
                return []
            
            valid_data = []
            for i, item in enumerate(data):
                if self.validate_term_data(item):
                    # Clean text fields
                    item['term'] = self.clean_text(item['term'])
                    item['definition'] = self.clean_text(item['definition'])
                    valid_data.append(item)
                else:
                    logger.warning(f"Invalid data at index {i}")
            
            logger.info(f"Loaded {len(valid_data)} valid terms from {filepath}")
            return valid_data
        
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return []
    
    def save_json_data(self, data: List[Dict[str, Any]], filepath: str):
        """Save data to JSON file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(data)} terms to {filepath}")
        except Exception as e:
            logger.error(f"Error saving to {filepath}: {e}")
    
    def convert_csv_to_json(self, csv_filepath: str, json_filepath: str):
        """Convert CSV data to JSON format."""
        try:
            data = []
            with open(csv_filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Map CSV columns to our schema
                    term_data = {
                        'term': row.get('term', ''),
                        'definition': row.get('definition', ''),
                        'source': row.get('source', 'Unknown'),
                        'category': row.get('category', ''),
                        'tags': row.get('tags', '').split(',') if row.get('tags') else [],
                        'url': row.get('url', ''),
                        'last_updated': row.get('last_updated', '')
                    }
                    
                    if self.validate_term_data(term_data):
                        # Clean text fields
                        term_data['term'] = self.clean_text(term_data['term'])
                        term_data['definition'] = self.clean_text(term_data['definition'])
                        data.append(term_data)
            
            self.save_json_data(data, json_filepath)
            logger.info(f"Converted {csv_filepath} to {json_filepath}")
        
        except FileNotFoundError:
            logger.error(f"CSV file not found: {csv_filepath}")
        except Exception as e:
            logger.error(f"Error converting CSV to JSON: {e}")
    
    def merge_datasets(self, input_files: List[str], output_file: str):
        """Merge multiple JSON datasets into one."""
        all_data = []
        seen_terms = set()
        
        for filepath in input_files:
            data = self.load_json_data(filepath)
            for item in data:
                term_lower = item['term'].lower()
                if term_lower not in seen_terms:
                    all_data.append(item)
                    seen_terms.add(term_lower)
                else:
                    logger.warning(f"Duplicate term found: {item['term']}")
        
        self.save_json_data(all_data, output_file)
        logger.info(f"Merged {len(input_files)} files into {output_file} with {len(all_data)} unique terms")
    
    def get_dataset_stats(self, filepath: str):
        """Get statistics about a dataset."""
        data = self.load_json_data(filepath)
        if not data:
            return
        
        stats = {
            'total_terms': len(data),
            'sources': {},
            'categories': {},
            'avg_definition_length': 0
        }
        
        total_length = 0
        for item in data:
            # Count sources
            source = item.get('source', 'Unknown')
            stats['sources'][source] = stats['sources'].get(source, 0) + 1
            
            # Count categories
            category = item.get('category', 'Uncategorized')
            stats['categories'][category] = stats['categories'].get(category, 0) + 1
            
            # Calculate definition length
            total_length += len(item['definition'])
        
        stats['avg_definition_length'] = total_length / len(data)
        
        print(f"\n📊 Dataset Statistics for {filepath}")
        print(f"Total Terms: {stats['total_terms']}")
        print(f"Average Definition Length: {stats['avg_definition_length']:.1f} characters")
        print(f"\nSources:")
        for source, count in sorted(stats['sources'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {source}: {count}")
        print(f"\nCategories:")
        for category, count in sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {category}: {count}")

def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Data processing utilities for Gov Terms AI")
    parser.add_argument('command', choices=['validate', 'convert', 'merge', 'stats', 'clean'],
                       help='Command to execute')
    parser.add_argument('--input', '-i', required=True, help='Input file(s)')
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Input format')
    
    args = parser.parse_args()
    
    processor = DataProcessor()
    
    if args.command == 'validate':
        data = processor.load_json_data(args.input)
        print(f"✅ Validation complete. {len(data)} valid terms found.")
    
    elif args.command == 'convert':
        if args.format == 'csv' and args.output:
            processor.convert_csv_to_json(args.input, args.output)
        else:
            print("❌ Convert requires CSV input and JSON output file")
    
    elif args.command == 'merge':
        input_files = args.input.split(',')
        if args.output:
            processor.merge_datasets(input_files, args.output)
        else:
            print("❌ Merge requires output file")
    
    elif args.command == 'stats':
        processor.get_dataset_stats(args.input)
    
    elif args.command == 'clean':
        data = processor.load_json_data(args.input)
        output_file = args.output or args.input.replace('.json', '_cleaned.json')
        processor.save_json_data(data, output_file)

if __name__ == "__main__":
    main()
