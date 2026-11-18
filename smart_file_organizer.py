from pathlib import Path

def get_directory():
    
    directory = Path(input("Enter the directory name: "))
    return directory #.name = gives me the directory name, returning the "Path" object

def validate_directory(name): # dealing with the path object
    if not name.exists():
        print("Directory doesn't exist")
    elif name.is_file():
        print("File not accepted. Only directory")
    elif not name.is_dir():
        print("Not a directory")
    else:
        print("Directory accepted")

def scan_directory(path):
    count = 0 
    for item in path.iterdir():
        if item.is_file():
            print(item.name)
            count += 1

    print(f"Total Files: {count}")

def identify_extension(path):
    print("Filename\tExtension\tCategory")
    for item in path.iterdir():
        if item.suffix:
           name = item.name
           extension = item.suffix.lower().strip()
           data = categorize_file()
           category = data.get(extension,"no")
           print(f"{name}\t\t{extension}\t\t{category}")
        else:
           print(f"{item.name}\t\tunknown\t\tunknown")

def categorize_file():
    categorize = {
        ".jpg":"Image",
        ".pdf":"Document",
        ".mp4":"Video",
        ".mp3":"Audio",
        ".txt":"Text",
        ".zip":"Archive",
        "":"unknown"
    }

    return categorize

 
def main():
  name = get_directory()
  validate_directory(name)
  scan_directory(name)
  identify_extension(name)
  
if __name__ == "__main__":
    main()