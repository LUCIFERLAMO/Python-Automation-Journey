from pathlib import Path

def get_directory():
    
    directory = Path(input("Enter the directory name: "))
    print(directory.name)

def main():
    get_directory()

if __name__ == "__main__":
    main()