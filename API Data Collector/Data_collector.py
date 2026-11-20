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
   

def extract_data(data):
   Extracted_data = []

   for row in data:
      e ={
         "id":row.get("id"),
         "title":row.get("title"),
         "body":row.get("body")
      }
      Extracted_data.append(e)
    
   print(f"Total data extracted: {len(Extracted_data)}")
   print("----------- Extracted Date --------------")
   for i in Extracted_data:
      print(i)
      print()


if result.status_code == 200:
    print("[+] Data collected")
    data = result.json()
    print(f"Total number of data retrived: {len(data)}")
    extract_data(data)
else:
    print("[-] Data not retrived")



   