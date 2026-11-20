
from urllib.parse import urlparse
import requests
import ssl
import socket
from datetime import datetime, timezone
import json
import csv


def validate_url():
    url = input("Enter the URL: ")
    result = urlparse(url)

    scheme = result.scheme
    hostname = result.hostname

    if scheme not in ["http", "https"]:
        print("[-] URL Rejected, only HTTP and HTTPS accepted")
        return

    if not hostname:
        print("[-] URL Rejected")
        return

    if result.username is not None or result.password is not None:
        print("[-] URL Rejected, no embedded credentials")
        return

    print(f"[+] Scheme: {scheme}")
    print(f"[+] hostname: {hostname}")
    print("[+] No Embeded Credentials Found")
    return url


def connect_website(url):
    try:
        data = requests.get(url, timeout=10)

    except requests.exceptions.Timeout:
        print("[-] Time out")
        return

    except requests.exceptions.ConnectionError:
        print("[-] Connection error")
        return

    except requests.exceptions.RequestException as error:
        print(f"[-] Request error: {error}")
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

    present = 0
    absent = 0
    results = {}

    for security_header in security_headers:
        if security_header in response.headers:
            print(f"[+] {security_header} present")
            present += 1
            value = response.headers.get(security_header)
            print(f"[+] Value: {value}")
            results[security_header] = value
        else:
            print(f"[-] {security_header} absent")
            absent += 1
            results[security_header] = None

    print(f"Total Present: {present}")
    print(f"Total absent: {absent}")

    return results


def inspect_tls(url):
    parse = urlparse(url)

    if parse.scheme != "https":
        print("[-] TLS inspection requires HTTPS")
        return {"status": "UNKNOWN", "reason": "URL is not HTTPS"}

    hostname = parse.hostname

    try:
        port = parse.port or 443
    except ValueError:
        print("[-] Invalid port")
        return {"status": "UNKNOWN", "reason": "Invalid port"}

    try:
        # establishing a tcp connection
        with socket.create_connection((hostname, port), timeout=10) as connection:

            # setting the settings for upgrading the tcp connection
            context = ssl.create_default_context()

            # upgrading the connection to TLS
            with context.wrap_socket(connection, server_hostname=hostname) as secure_connection:

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
                print(f"warning, only {int(days_left)} days left" if days_left < 30 else "Valid")

                return {
                    "status": "PASS",
                    "issuer": str(issuer),
                    "expiry": expiry,
                    "days_left": int(days_left)
                }

    except socket.timeout:
        print("[-] Time out")
        return {"status": "UNKNOWN", "reason": "Connection timed out"}

    except ssl.SSLCertVerificationError:
        print("[-] Certificate verification failed")
        return {"status": "FAIL", "reason": "Certificate verification failed"}

    except (ssl.SSLError, OSError) as error:
        print(f"[-] TLS connection error: {error}")
        return {"status": "UNKNOWN", "reason": str(error)}


def check_https_redirect(url):
    data = urlparse(url)
    hostname = data.hostname

    try:
        port = data.port
    except ValueError:
        return {"status": "UNKNOWN", "reason": "Invalid port"}

    # Build the HTTP URL without adding another .com
    http_url = f"http://{hostname}"

    if port and port not in [80, 443]:
        http_url = f"http://{hostname}:{port}"

    try:
        response = requests.get(
            http_url,
            timeout=10,
            allow_redirects=False
        )

        print("[+] Status Code:", response.status_code)
        print("[+] URL:", response.url)

        location = response.headers.get("Location")
        print("[+] Redirect Location:", location)

        if response.is_redirect and location:
            from urllib.parse import urljoin

            final_url = urljoin(response.url, location)
            final_data = urlparse(final_url)

            if final_data.scheme == "https":
                print("[+] HTTP - HTTPS conversion Successful")
                return {
                    "status": "PASS",
                    "http_url": http_url,
                    "destination": final_url,
                    "status_code": response.status_code
                }

            else:
                print("[-] HTTP - HTTPS conversion Unsuccessful")
                return {
                    "status": "FAIL",
                    "http_url": http_url,
                    "destination": final_url,
                    "status_code": response.status_code
                }

        else:
            print("[-] No HTTP to HTTPS redirect detected")
            return {
                "status": "FAIL",
                "http_url": http_url,
                "destination": None,
                "status_code": response.status_code
            }

    except requests.exceptions.RequestException as error:
        print(f"[-] Redirect check failed: {error}")
        return {"status": "UNKNOWN", "reason": str(error)}


def inspect_cookies(response):
    results = []

    if len(response.cookies) == 0:
        print("[-] No cookies found")
        return results

    for cookie in response.cookies:
        secure = cookie.secure
        httponly = cookie.has_nonstandard_attr("HttpOnly")
        samesite = cookie.get_nonstandard_attr("SameSite")

        print("Name:", cookie.name)
        print("Secure:", "ENABLED" if secure else "MISSING")
        print("HttpOnly:", "ENABLED" if httponly else "MISSING")
        print("SameSite:", samesite if samesite else "MISSING")
        print()

        results.append({
            "name": cookie.name,
            "secure": secure,
            "httponly": httponly,
            "samesite": samesite
        })

    return results




def analyze_findings(headers, tls, redirects, cookies):
    findings = []

    print("\n========== SECURITY FINDINGS ==========\n")

    def add_finding(check, status, severity, description):
        findings.append({
            "check": check,
            "status": status,
            "severity": severity,
            "description": description
        })

    if tls["status"] == "FAIL":
        add_finding(
            "TLS Certificate",
            "FAIL",
            "HIGH",
            tls.get("reason", "Certificate verification failed")
        )

    elif tls["status"] == "UNKNOWN":
        add_finding(
            "TLS Certificate",
            "UNKNOWN",
            "NONE",
            tls.get("reason", "TLS inspection could not be completed")
        )

    elif tls.get("days_left", 100) < 30:
        add_finding(
            "TLS Certificate Expiration",
            "FAIL",
            "MEDIUM",
            "Certificate expires in fewer than 30 days"
        )

    if redirects["status"] == "FAIL":
        add_finding(
            "HTTPS Redirect",
            "FAIL",
            "MEDIUM",
            "HTTP does not directly redirect to HTTPS"
        )

    elif redirects["status"] == "UNKNOWN":
        add_finding(
            "HTTPS Redirect",
            "UNKNOWN",
            "NONE",
            "Redirect inspection could not be completed"
        )

    header_rules = {
        "Content-Security-Policy": "MEDIUM",
        "Strict-Transport-Security": "MEDIUM",
        "X-Content-Type-Options": "LOW",
        "Referrer-Policy": "LOW"
    }

    for header, severity in header_rules.items():
        if headers.get(header) is None:
            add_finding(
                header,
                "FAIL",
                severity,
                f"{header} header is missing"
            )

    # Cookie purpose cannot be reliably identified from its name alone.
    # Missing attributes are therefore marked for review.
    for cookie in cookies:
        if not cookie["secure"]:
            add_finding(
                f"Cookie: {cookie['name']}",
                "REVIEW",
                "NONE",
                "Secure attribute missing; check whether cookie is sensitive"
            )

        if not cookie["httponly"]:
            add_finding(
                f"Cookie: {cookie['name']}",
                "REVIEW",
                "NONE",
                "HttpOnly attribute missing; check whether JavaScript access is required"
            )

        if not cookie["samesite"]:
            add_finding(
                f"Cookie: {cookie['name']}",
                "REVIEW",
                "NONE",
                "SameSite attribute missing; review cross-site cookie behavior"
            )

    high = 0
    medium = 0
    low = 0
    unknown = 0
    review = 0

    for finding in findings:
        print(f"[{finding['severity']}] {finding['check']}")
        print(f"Status: {finding['status']}")
        print(f"Description: {finding['description']}")
        print()

        if finding["severity"] == "HIGH":
            high += 1
        elif finding["severity"] == "MEDIUM":
            medium += 1
        elif finding["severity"] == "LOW":
            low += 1

        if finding["status"] == "UNKNOWN":
            unknown += 1
        elif finding["status"] == "REVIEW":
            review += 1

    print("---------- SECURITY SUMMARY ----------")
    print("HIGH Findings:", high)
    print("MEDIUM Findings:", medium)
    print("LOW Findings:", low)
    print("Unknown Checks:", unknown)
    print("Items for Review:", review)
    print("Total Findings:", len(findings))
    print("======================================")

    return findings

def save_report(url, headers, tls, redirects, cookies, findings):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    report = {
        "target": url,
        "timestamp": timestamp,
        "security_headers": headers,
        "tls": tls,
        "https_redirect": redirects,
        "cookies": cookies,
        "findings": findings
    }

    json_file = f"security_report_{timestamp}.json"
    csv_file = f"security_findings_{timestamp}.csv"

    print("\n========== SAVING REPORT ==========\n")

    try:
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)

        print(f"[+] JSON report saved: {json_file}")

    except OSError as error:
        print(f"[-] JSON file error: {error}")

    try:
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["check", "status", "severity", "description"]
            )

            writer.writeheader()
            writer.writerows(findings)

        print(f"[+] CSV report saved: {csv_file}")

    except (OSError, csv.Error) as error:
        print(f"[-] CSV file error: {error}")

    print("======================================\n")


if __name__ == "__main__":
    url = validate_url()

    if url:
        response = connect_website(url)

        if response is not None:
            print("\n========== HTTPS REDIRECT ==========\n")
            redirects = check_https_redirect(url)

            print("\n========== COOKIE INSPECTION ==========\n")
            cookies = inspect_cookies(response)

            print("\n========== SECURITY HEADERS ==========\n")
            headers = check_security_headers(response)

            print("\n========== TLS INSPECTION ==========\n")
            tls = inspect_tls(url)

            findings = analyze_findings(headers, tls, redirects, cookies)

            save_report(url, headers, tls, redirects, cookies, findings)
