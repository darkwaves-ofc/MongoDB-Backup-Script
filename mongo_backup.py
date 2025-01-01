import os
import subprocess
import json
import sys
import logging
import argparse
from pymongo import MongoClient

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def install_dependencies():
    """Ensures all required Python dependencies are installed."""
    try:
        import pymongo
    except ImportError:
        logger.info("Installing required dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pymongo"])
        logger.info("Dependencies installed successfully.")

# Check and install dependencies
install_dependencies()

def get_input(prompt, default_value=None, is_list=False):
    """Prompts for user input or returns a default value."""
    if is_list:
        return input(prompt).split(',')
    return input(prompt) or default_value

def backup_mongo_database(MONGO_URI, DB_NAMES, MONGO_TOOLS_PATH, BACKUP_DIR):
    """Exports the specified MongoDB databases into JSON files."""
    for DB_NAME in DB_NAMES:
        OUTPUT_DIR = os.path.join(BACKUP_DIR, DB_NAME)

        # Ensure the output directory exists
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        # Connect to MongoDB to get collection names
        try:
            client = MongoClient(MONGO_URI)
            db = client[DB_NAME]
            collections = db.list_collection_names()
            logger.info(f"Found collections in {DB_NAME}: {collections}")
        except Exception as e:
            logger.error(f"Error connecting to MongoDB database {DB_NAME}: {e}")
            continue

        # Export each collection and convert to JSON
        for collection in collections:
            logger.info(f"Exporting collection: {collection} from {DB_NAME}...")
            ndjson_file = os.path.join(OUTPUT_DIR, f"{collection}.ndjson")
            json_file = os.path.join(OUTPUT_DIR, f"{collection}.json")

            try:
                # Export collection as NDJSON using mongoexport
                subprocess.run([
                    os.path.join(MONGO_TOOLS_PATH, "mongoexport"),
                    f"--uri={MONGO_URI}",
                    f"--db={DB_NAME}",
                    f"--collection={collection}",
                    f"--out={ndjson_file}"
                ], check=True)

                # Convert NDJSON to JSON array
                with open(ndjson_file, 'r') as ndjson_f, open(json_file, 'w') as json_f:
                    json_docs = [json.loads(line) for line in ndjson_f]
                    json.dump(json_docs, json_f, indent=4)

                logger.info(f"Successfully exported: {collection} -> {json_file}")
                os.remove(ndjson_file)  # Clean up intermediate NDJSON
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to export collection: {collection} from {DB_NAME}. Error: {e}")
            except Exception as e:
                logger.error(f"Error processing collection {collection} from {DB_NAME}: {e}")

        logger.info(f"All collections from {DB_NAME} exported to {OUTPUT_DIR} in valid JSON format.")

    logger.info("Export completed for all databases.")

def main():
    parser = argparse.ArgumentParser(description="MongoDB Backup Script")
    parser.add_argument("--uri", help="MongoDB URI", required=True)
    parser.add_argument("--databases", help="Comma-separated list of databases to back up", required=True)
    parser.add_argument("--backup-dir", help="Directory to store backups", default=os.path.join(os.getcwd(), "database_backup"))
    parser.add_argument("--tools-path", help="Path to MongoDB tools", default=os.path.join(os.getcwd(), "mongodb-database-tools", "bin"))
    
    args = parser.parse_args()

    MONGO_URI = args.uri
    DB_NAMES = args.databases.split(',')
    MONGO_TOOLS_PATH = args.tools_path
    BACKUP_DIR = args.backup_dir

    # Ensure backup directory exists
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    backup_mongo_database(MONGO_URI, DB_NAMES, MONGO_TOOLS_PATH, BACKUP_DIR)

if __name__ == "__main__":
    main()
