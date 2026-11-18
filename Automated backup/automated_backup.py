from pathlib import Path 

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
        

def main():
    source,destination = getpaths()
    result = validate_Source(source)
    if result:
       r1 = prepare_destination(source,destination)
       if r1:
         pass

if __name__ == "__main__":
    main()

