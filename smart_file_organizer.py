from pathlib import Path

def get_directory():
    
    directory = Path(input("Enter the directory name: "))
    return directory #.name = gives me the directory name, returning the "Path" object

def validate_directory(name): # dealing with the path object
    if not name.exists():
        print("Directory dosent exist")
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

def identify_extention(path):
    for item in path.iterdir():
        if item.suffix:
           print(item.suffix.lower())
        else: 
            print(f"No Extention for: {item.name}")



 
def main():
  name = get_directory()
  validate_directory(name)
  scan_directory(name)
  identify_extention(name)
  
if __name__ == "__main__":
    main()