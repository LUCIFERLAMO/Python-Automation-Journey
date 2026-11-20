# Python Automation Journey

This repository contains small Python automation projects.

## Smart File Organizer

`smart_file_organizer.py` is a Python command-line tool that organizes files from a selected directory into category folders based on their file extensions.

### Features

- Accepts a directory path from the user
- Validates that the path exists and is a directory
- Counts files in the selected directory
- Categorizes files by extension
- Creates category folders automatically
- Moves files into matching folders
- Moves files without extensions or known categories into an `unknown` folder
- Prints the organization results in a table

### Supported Categories

| Extension | Category |
|-----------|----------|
| `.jpg` | Image |
| `.pdf` | Document |
| `.mp4` | Video |
| `.mp3` | Audio |
| `.txt` | Text |
| `.zip` | Archive |

### Usage

Run the program from a terminal:

```bash
python smart_file_organizer.py
```

## API Data Collector

`API Data Collector/Data_collector.py` collects posts from the JSONPlaceholder API for a selected user ID.

### Features

- Accepts a user ID between 1 and 10
- Fetches matching posts from the API
- Handles timeout, connection, and HTTP errors
- Extracts post ID, title, and body
- Saves the extracted data as JSON and CSV

### Usage

```bash
python "API Data Collector/Data_collector.py"
```

The JSON output is saved as `posts_under_<userId>`, and the CSV output is saved as `posts_<userId>.csv`.
