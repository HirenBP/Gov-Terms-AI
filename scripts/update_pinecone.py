"""
Script to update Pinecone index 'multilingual-e5-large-index' in namespace 'gov-terms' from combined_glossary.json.
Assumes Pinecone handles embedding generation (field: 'text').
"""

import os
import json
import logging
from pinecone import Pinecone

# Config
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = "all-e5-large"
PINECONE_NAMESPACE = "gov-terms2"
GLOSSARY_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "combined_glossary.json")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("update_pinecone")

if not PINECONE_API_KEY:
    raise RuntimeError("PINECONE_API_KEY environment variable not set.")

# Load data
with open(GLOSSARY_PATH, encoding="utf-8") as f:
    records = json.load(f)

logger.info(f"Loaded {len(records)} records from {GLOSSARY_PATH}")

# Prepare Pinecone records
pinecone_records = []
for i, rec in enumerate(records):
    # Compose a unique id: term_01, term_02, ...  
    rec_id = f"term_{i+1:02d}"
    Term = rec.get("Term", "")
    Definition = rec.get("Definition", "")
    text = Term + ": " + Definition
    Entity = rec.get("Entity", "")
    Portfolio = rec.get("Portfolio", "")
    BodyType = rec.get("BodyType", "")
    Url = rec.get("Url", "")

    if not text:
        logger.warning(f"Skipping record {rec_id}: no term.")
        continue
    # Add all fields as metadata
    pinecone_record = {
        "_id": rec_id, 
        "text": text,
        "Definition": Defintion,
        "Entity": Entity,
        "Portfolio": Portfolio,
        "BodyType": BodyType,
        "Url": Url}
    for k, v in rec.items():
        if k != "Term":
            pinecone_record[k] = v
    pinecone_records.append(pinecone_record)

logger.info(f"Prepared {len(pinecone_records)} records for Pinecone upsert.")

# Upsert to Pinecone using upsert_records (recommended for serverless)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

# Insert the first record and ask for confirmation
first_record = pinecone_records[0:1]
logger.info(f"About to upsert the first record: {first_record[0]}")
index.upsert_records(PINECONE_NAMESPACE, first_record)
logger.info("First record upserted.")

confirm = input("Do you want to continue upserting the remaining records in batches? (y/n): ").strip().lower()
if confirm != 'y':
    logger.info("Aborting batch upsert as per user request.")
    exit(0)

BATCH_SIZE = 90
for i in range(1, len(pinecone_records), BATCH_SIZE):
    batch = pinecone_records[i:i+BATCH_SIZE]
    index.upsert_records(PINECONE_NAMESPACE, batch)
    logger.info(f"Upserted records {i+1}-{min(i+BATCH_SIZE, len(pinecone_records))}")
logger.info("Pinecone index update complete.")
