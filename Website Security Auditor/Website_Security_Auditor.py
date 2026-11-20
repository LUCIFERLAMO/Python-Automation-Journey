from urllib.parse import urlparse
import requests
import ssl
import socket
from datetime import datetime, timezone

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

def inspect_tls(url):
    parse = urlparse(url)

    if parse.scheme == "https":
        hostname = parse.hostname
        port = 443
        try:
            # establishing a tcp connection
            with socket.create_connection((hostname,port),timeout=10) as connection:

                # setting the settings for upgrading the tcp connection
                context = ssl.create_default_context()

                #upgrading the connection -> use the context setting and wrap the connectin to make the tcp connection here the TCP handshake happnes
                with context.wrap_socket(connection,server_hostname=hostname)as secure_connection:

                    # retriving the TLS certificate
                    certificate = secure_connection.getpeercert()

                    # Extract certificate information
                    issuer = certificate["issuer"]
                    expiry = certificate["notAfter"]

                    # Convert expiry date to timestamp
                    expiry_timestamp = ssl.cert_time_to_seconds(expiry)

                    # Get current timestamp
                    current_timestamp = datetime.now(timezone.utc).timestamp()

                    # Calculate remaining days
                    days_left = (expiry_timestamp - current_timestamp) / 86400

                    # Display results
                    print("TLS Connection: Successful")
                    print("Certificate Issuer:", issuer)
                    print("Expiry Date:", expiry)
                    print("Days Remaining:", int(days_left))
                    print(f"warning, only {int(days_left)} " if int(days_left) < 30 else "Valid")
        except TimeoutError:
            print("[-] Time out")
        except ssl.SSLCertVerificationError:
            print("[-] certificate verification failed")

def check_https_redirect(url):
    data = urlparse(url)
    hostname = data.hostname

    http_url = f"http://{hostname}.com"

    response = requests.get(http_url,timeout=10)

    for redirect in response.history:
      print("[+] Status Code:", redirect.status_code)
      print("[+] URL:", redirect.url)
      print("[+] Redirect Location:", redirect.headers.get("Location"))
      final_url = urlparse(redirect.headers.get("Location"))
      if final_url.scheme == "https":
          print("[+] HTTP - HTTPS converstion Successful")
      else:
          print("[-] HTTP -HTTPS conversion Unsuccessful")
      

    
if __name__ == "__main__":
    url = validate_url()
    if url:
        response = connect_website(url)
        check_https_redirect(url)
        check_security_headers(response)
        inspect_tls(url)