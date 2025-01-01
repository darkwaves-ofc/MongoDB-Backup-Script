# MongoDB Backup Tool

A versatile Python-based MongoDB backup solution that offers both a graphical user interface (GUI) and command-line interface (CLI) for backing up MongoDB databases to JSON files. This tool exports collections from specified MongoDB databases into readable JSON format using `mongoexport`.

## Screenshot

![Banner](https://github.com/darkwaves-ofc/MongoDB-Backup-Script/blob/94d60bc91a3dda54ded0e5b4583f43b15b197651/screenshot/image.png)
![Banner2](https://github.com/darkwaves-ofc/MongoDB-Backup-Script/blob/96c9faddd2423e56f5a2f7478a52f3ed29eddf0e/screenshot/image2.png)

## Features
- **Command-line interface**: Allows you to specify MongoDB URI, databases to back up, and other configurations.
- **Database Export**: Exports collections from specified MongoDB databases into `.json` files.
- **Logging**: Logs the process to track successes and failures.
- **Error Handling**: Provides robust error handling during MongoDB connection and export operations.

### GUI Version (`mongo_backup_gui.py`)
- User-friendly graphical interface
- Real-time backup progress tracking
- Multi-database selection
- Connection testing capability
- Interactive file/directory selection
- Live logging window
- Multi-threaded operations to prevent UI freezing

### CLI Version (`mongo_backup.py`)
- Command-line interface for automation and scripting
- Support for multiple database backups
- Detailed logging
- Configurable backup paths
- Error handling and reporting

## Requirements

- Python 3.6+
- MongoDB tools (including `mongoexport`)
- Dependencies: 
  - `pymongo`
  - `tkinter` (for GUI version)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/mongo-backup-tool.git
   cd mongo-backup-tool
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   The scripts will automatically install required dependencies if not present.

3. **MongoDB Tools**:
   Ensure MongoDB tools (including `mongoexport`) are installed on your system.

## Usage

### GUI Version

1. **Launch the GUI**:
   ```bash
   python mongo_backup_gui.py
   ```

2. **Using the GUI**:
   - Enter your MongoDB URI
   - Click "Test Connection" to verify connectivity
   - Select databases to backup from the list
   - Choose MongoDB tools path and backup directory
   - Click "Start Backup" to begin the process
   - Monitor progress in real-time through the progress bar and log window

### CLI Version

Run the script with the following command:

```bash
python mongo_backup.py --uri "<MongoDB_URI>" --databases "<Database_1>,<Database_2>" --backup-dir "<Backup_Directory>" --tools-path "<MongoDB_Tools_Path>"
```

#### Command-line arguments:

- `--uri`: MongoDB URI (required)
  Example: `mongodb+srv://username:password@cluster0.mongodb.net`
  
- `--databases`: Comma-separated list of databases to back up (required)
  Example: `appointment,cdn`
  
- `--backup-dir`: Backup directory path (default: `./database_backup`)

- `--tools-path`: MongoDB tools path (default: `./mongodb-database-tools/bin`)

#### Example:
```bash
python mongo_backup.py --uri "mongodb+srv://username:password@cluster0.mongodb.net" --databases "appointment,cdn" --backup-dir "./backups" --tools-path "./mongodb-database-tools/bin"
```

## How it works

1. **Connection**: The tool connects to MongoDB using the provided URI
2. **Database Selection**: 
   - GUI: Select databases from the interactive list
   - CLI: Specify databases via command-line arguments
3. **Export Process**: 
   - Uses `mongoexport` to extract collections
   - Converts data to formatted JSON files
   - Organizes backups in the specified directory
4. **Progress Tracking**:
   - GUI: Real-time progress bar and log window
   - CLI: Terminal-based logging

## Output Structure

```
backup_directory/
├── database1/
│   ├── collection1.json
│   ├── collection2.json
│   └── collection3.json
└── database2/
    ├── collection1.json
    └── collection2.json
```

## Troubleshooting

### Common Issues:
- **Connection Failed**: Verify MongoDB URI and network connectivity
- **Export Error**: Ensure `mongoexport` is properly installed and path is correct
- **Permission Error**: Check write permissions for backup directory
- **GUI Not Loading**: Verify tkinter is installed (`pip install tk`)

### For GUI Users:
- Use the "Test Connection" button to verify MongoDB connectivity
- Check the log window for detailed error messages
- Ensure all paths are correctly set before starting backup

### For CLI Users:
- Review command-line arguments for accuracy
- Check console output for error messages
- Verify database names are correctly comma-separated

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Vimukthi Indunil  
[GitHub](https://github.com/darkwaves-ofc)
