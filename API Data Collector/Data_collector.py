import requests
import json
import csv

def get_data(parameter):
  url = "https://jsonplaceholder.typicode.com/posts"
  p = {"userId":parameter}
  try: 
    print("[+] Fetching data")
    result = requests.get(url,timeout=10,params=p)
    result.raise_for_status()
  except requests.exceptions.Timeout:
     print("[-] Time out")
     return
  except requests.exceptions.ConnectionError:
     print("[-] Connection error")
     return
  except requests.exceptions.HTTPError:
     print(f"[-] Status code: {result.status_code}")
     print("[-] detects an HTTP error")
     return
  if result.status_code == 200:
    print("[+] Data collected")
    data = result.json()
    print(f"Total number of data retrived: {len(data)}")
    return data
  else:
    print("[-] Data not retrived")  
     
     
def get_userID():
  try:
    userid = int(input("Enter the userID (1/10): "))
  except ValueError:
    print("[-] Value error only int accepted")
    return 
  if 0 <= userid <=10 : # chain operation 
    return userid
  else:
    print("[-] userId is not with in 0-10")
    return
  

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

   return Extracted_data

def save_json(data, userId):
  file_name = f"posts_under_{userId}"
  with open(file_name, "w")as f:
    json.dump(data,f,indent=4)
  print(f"[+] Data saved: {file_name}")

def save_csv(data,userId):
  file_name = f"posts_{userId}.csv"
  with open(file_name,"w",newline="",encoding="utf-8" )as f:
    writer = csv.DictWriter(f,fieldnames=["id","title","body"]) # shd be same as the key, no upper case.
    writer.writeheader()
    writer.writerows(data)

if __name__ == "__main__":
  userid = get_userID()
  if userid:
    data = get_data(userid)
    if data: 
      extracted_data = extract_data(data)
      save_json(extracted_data,userid)
      save_csv(extracted_data,userid)


   