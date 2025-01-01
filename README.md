
# MongoDB Backup Script

This Python script allows you to back up MongoDB databases to JSON files. It exports all collections from specified MongoDB databases into JSON format using `mongoexport` and processes them into readable files.

## Features
- **Command-line interface**: Allows you to specify MongoDB URI, databases to back up, and other configurations.
- **Database Export**: Exports collections from specified MongoDB databases into `.json` files.
- **Logging**: Logs the process to track successes and failures.
- **Error Handling**: Provides robust error handling during MongoDB connection and export operations.

## Requirements

- Python 3.6+
- MongoDB tools (including `mongoexport`)
- Dependencies: `pymongo` (installed automatically if not present)

## Installation

1. **Clone the repository** (if applicable):
   ```bash
   git clone https://github.com/yourusername/mongo-backup-script.git
   cd mongo-backup-script
   ```

2. **Install dependencies**:
   Make sure you have the required dependencies installed. Run the following command to install them:
   ```bash
   pip install -r requirements.txt
   ```

   Alternatively, the script will automatically install the `pymongo` dependency if not present.

3. **MongoDB Tools**:
   Ensure you have MongoDB tools (including `mongoexport`) installed on your system. The script assumes that `mongoexport` is available at the path specified by `--tools-path`.

## Usage

To run the script, use the following command:

```bash
python mongo_backup.py --uri "<MongoDB_URI>" --databases "<Database_1>,<Database_2>" --backup-dir "<Backup_Directory>" --tools-path "<MongoDB_Tools_Path>"
```

### Command-line arguments:

- `--uri`: MongoDB URI to connect to the database (required).
  Example: `mongodb+srv://username:password@cluster0.mongodb.net`
  
- `--databases`: Comma-separated list of databases to back up (required).
  Example: `appointment,cdn`
  
- `--backup-dir`: Directory where the backups will be saved (default: `./database_backup`).

- `--tools-path`: Path to MongoDB tools, including `mongoexport` (default: `./mongodb-database-tools/bin`).

### Example:

```bash
python mongo_backup.py --uri "mongodb+srv://username:password@cluster0.mongodb.net" --databases "appointment,cdn" --backup-dir "./backups" --tools-path "./mongodb-database-tools/bin"
```

## How it works:

1. **Install Dependencies**: The script checks for the `pymongo` library and installs it if not already installed.
2. **MongoDB Connection**: The script connects to MongoDB using the URI you provide.
3. **Database Export**: It exports the collections from the specified databases using `mongoexport`, then converts them to JSON files.
4. **Backup Directory**: The exported collections are saved as `.json` files in the backup directory.
5. **Logging**: The script logs the status of each operation, including success and errors.

## Troubleshooting

- Ensure that you have the correct MongoDB URI and that the databases are accessible.
- Ensure `mongoexport` is available on your system and its path is correctly set.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Your Name  
[Your Website](https://yourwebsite.com)  
[Your GitHub](https://github.com/yourusername)

