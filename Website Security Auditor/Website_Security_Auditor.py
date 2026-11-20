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
    return data

def check_security_headers(response):
    security_headers = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy"
   ]

    present=0
    absent=0

    for security_header in security_headers:
        if security_header in response:
            print(f"[+] {security_header} present")
            present+=1
            value = response.get(security_header)
            print(f"[+] Value: {value}")
        else:
            print(f"[-] {security_header} absent")
            absent+=1

    print(f"Total Present: {present}")
    print(f"Total absent: {absent}")
    
if __name__ == "__main__":
    url = validate_url()
    if url:
        response = connect_website(url)
        check_security_headers(response)