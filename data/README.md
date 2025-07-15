# Data Directory

This directory contains datasets and data files for the Gov Terms AI project.

## Files

### `sample_gov_terms.json`
Sample government terms and definitions for testing and development. Contains 10 example terms with proper formatting and metadata.

## Data Format

All term data should follow this JSON schema:

```json
{
  "term": "string (required)",
  "definition": "string (required, min 10 characters)",
  "source": "string (required)",
  "url": "string (optional)",
  "category": "string (optional)",
  "tags": ["array of strings (optional)"],
  "last_updated": "string (optional, ISO date format)"
}
```

## Directory Structure

```
data/
├── README.md                 # This file
├── sample_gov_terms.json     # Sample data for testing
├── raw/                      # Raw scraped data (create as needed)
├── processed/                # Cleaned and processed data
├── embeddings/               # Generated embeddings
└── archive/                  # Archived/backup data
```

## Data Sources

- Government websites (usa.gov, regulations.gov, etc.)
- Legislative documents
- Federal agency publications
- Congressional Research Service reports
- Administrative procedure documentation

## Data Processing Pipeline

1. **Collection**: Scrape or import raw data
2. **Validation**: Check required fields and data quality
3. **Cleaning**: Normalize text, remove artifacts
4. **Enrichment**: Add categories, tags, metadata
5. **Embedding**: Generate vector embeddings
6. **Upload**: Store in Pinecone vector database

## Quality Guidelines

- Definitions should be comprehensive (50+ characters recommended)
- Terms should be unique (case-insensitive)
- Sources must be credible government or academic sources
- URLs should be permanent links when possible
- Categories should be consistent across the dataset
- Tags should be lowercase and descriptive

## Usage with ML Pipeline

```bash
# Process raw data
python scripts/data_utils.py clean -i data/raw/terms.json -o data/processed/terms.json

# Generate embeddings
python ml-pipeline/generate_embeddings.py --input data/processed/terms.json

# Upload to Pinecone
python ml-pipeline/upload_to_pinecone.py --input data/processed/terms.json
```

## Legal and Ethical Considerations

- Ensure all data sources are properly attributed
- Respect copyright and intellectual property rights
- Follow fair use guidelines for government information
- Maintain data accuracy and currency
- Protect any sensitive or classified information
