from pathlib import Path
import shutil

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
            count += 1

    return count

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

def identify_extension(path):
    print("Filename\tExtension\tCategory")
    for item in path.iterdir():
        if item.suffix and item.is_file():
           name = item.name
           extension = item.suffix.lower().strip()
           data = categorize_file()
           category = data.get(extension,"no")
           create_category_folder(path,category)
           full_path = path / category
           move_file(item,full_path)
           print(f"{name}\t\t{extension}\t\t{category}")
        elif not item.is_dir():
           print(f"{item.name}\t\tunknown\t\tunknown")

    c = scan_directory(path)
    print(f"Total Files: {c}")


def create_category_folder(path, category):
    full_path = path / category
    if not full_path.exists():
        full_path.mkdir(exist_ok=True)

  

def move_file(source_file_path, destination_folder_path):
    source_file_name = source_file_path.name
    final = destination_folder_path / source_file_name
    if not final.exists():
        shutil.move(source_file_path,destination_folder_path)
        


def main():
  name = get_directory()
  validate_directory(name)
  identify_extension(name)
  
  
if __name__ == "__main__":
    main()