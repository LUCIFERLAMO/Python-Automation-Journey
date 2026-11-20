from urllib.parse import urlparse
import requests

def validate_url():
    url = input("Enter the URL: ")
    result = urlparse(url)

    scheme = result.scheme
    hostname = result.hostname
    if not hostname:
        print("[-] URL Rejected")
        return

    if result.username or result.password:
        print("[-] URL Rejected, no embedded credentials")
        return

    print(f"[+] Scheme: {scheme}")
    print(f"[+] hostname: {hostname}")
    print("[+] No Embeded Credentials Found")
    return url

def connect_website(url):
    try:
       data = requests.get(url,timeout=10)
    except TimeoutError:
        print("Time out")
        return 
    except ConnectionError:
        print("Connection error")
        return
    except Exception:
        print("Remove this and find out the expection")
        return

    print(f"Status code: {data.status_code}")
    print(f"Final Url: {data.url}")
    return True

if __name__ == "__main__":
    url = validate_url()
    if url:
        connect_website(url)