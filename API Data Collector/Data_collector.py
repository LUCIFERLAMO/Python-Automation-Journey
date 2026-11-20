import requests

url = "https://jsonplaceholder.typicode.com/posts"

result = requests.get(url)

if result.status_code == 200:
    print("[+] Data collected")
    data = result.json()
    print(f"Total number of data retrived: {len(data)}")
    print("[+] Title of the first post")
    print(data[0]["title"])
else:
    print("[-] Data not retrived")