from pathlib import Path

def get_directory():
    
    directory = Path(input("Enter the directory name: "))
    return directory #.name = gives me the directiry name, returning the "Path" object

def validate_directory(name): # dealing with the path object
    if not name.exists():
        print("Directory dosent exist")
    elif name.is_file():
        print("File not accepted. Only directory")
    elif not name.is_dir():
        print("Not a directory")
    else:
        print("Directory accepted")
       
 
def main():
  name = get_directory()
  validate_directory(name)

if __name__ == "__main__":
    main()