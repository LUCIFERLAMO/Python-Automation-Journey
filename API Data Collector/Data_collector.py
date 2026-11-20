import requests

url = "https://jsonplaceholder.typicode.com/posts"
try: 
  print("[+] Fetching data")
  result = requests.get(url,timeout=10)
  result.raise_for_status()
except requests.exceptions.Timeout:
   print("[-] Time out")
except requests.exceptions.ConnectionError:
   print("[-] Connection error")
except requests.exceptions.HTTPError:
   print(f"[-] Status code: {result.status_code}")
   print("[-] detects an HTTP error")
   

if result.status_code == 200:
    print("[+] Data collected")
    data = result.json()
    print(f"Total number of data retrived: {len(data)}")
    print("[+] Title of the first post")
    print(data[0]["title"])
else:
    print("[-] Data not retrived")