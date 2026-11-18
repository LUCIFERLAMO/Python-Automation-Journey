# Smart File Organizer

`smart_file_organizer.py` is a Python command-line tool that organizes files from a selected directory into category folders based on their file extensions.

## Features

- Accepts a directory path from the user
- Validates that the path exists and is a directory
- Counts files in the selected directory
- Categorizes files by extension
- Creates category folders automatically
- Moves files into matching folders
- Moves files without extensions or known categories into an `unknown` folder
- Prints the organization results in a table

## Supported Categories

| Extension | Category |
|-----------|----------|
| `.jpg` | Image |
| `.pdf` | Document |
| `.mp4` | Video |
| `.mp3` | Audio |
| `.txt` | Text |
| `.zip` | Archive |

## Usage

Run the program from a terminal:

```bash
python smart_file_organizer.py
```

Enter the path of the directory you want to organize when prompted.