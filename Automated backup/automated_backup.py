from pathlib import Path 
from datetime import datetime
import shutil

def getpaths():
    source = Path(input("Enter the source Path: "))
    destination = Path(input("Enter the destination path: "))

    return source,destination

def validate_Source(source):
    if not source.exists():
        print("[-] Invalid Source")
        return False
    elif not source.is_dir():
        print("[-] Source is not a Directory")
        return False
    else:
        print("[+] Source accepted")
        return True

def prepare_destination(source,destination):
    if not destination.is_dir():
        print("[-] Destination is not a Directory")
        return False 
    elif destination == source:
        print("[-] Destination cant be the source")
        return False 
    elif destination.resolve().is_relative_to(source.resolve()):
        print("[-] Destination cannot be inside the source")
        return False
    elif not destination.exists():
        print("[-] Destination does not exist")
        print("[+] Creating the destination path")
        destination.mkdir()
        print("[+] Destination path created")
        return True
    else:
        print("[+] Destination Exists")
        return True

def create_backup(source, destination):
    name = source.name
    time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    final_file_name = f"{name}_{time}"
    print("[+] creating the zip file")
    shutil.make_archive(destination/final_file_name, "zip", source )
    print(f"[+] Zip file created in loc {destination}")


def main():
    source,destination = getpaths()
    result = validate_Source(source)
    if result:
       r1 = prepare_destination(source,destination)
       if r1:
         create_backup(source,destination)

if __name__ == "__main__":
    main()

