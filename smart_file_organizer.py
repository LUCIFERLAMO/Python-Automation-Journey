from pathlib import Path
import shutil

def get_directory():
    
    directory = Path(input("Enter the directory name: "))
    return directory #.name = gives me the directory name, returning the "Path" object

def validate_directory(name): # dealing with the path object
    if not name.exists():
        print("Directory doesn't exist")
        return False 
    elif name.is_file():
        print("File not accepted. Only directory")
        return False 
    elif not name.is_dir():
        print("Not a directory")
        return False 
    else:
        print("Directory accepted")
        return True

def scan_directory(path):
    count = 0 
    for item in path.iterdir():
        if item.is_file():
            count += 1

    print(f"total files: {count}")

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
           create_category_folder(path,"unknown")
           f = path / "unknown"
           move_file(item,f)


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
  result = validate_directory(name)
  if result: 
    scan_directory(name)
    identify_extension(name)
  else: 
      print("Not accepted")
  
  
if __name__ == "__main__":
    main()