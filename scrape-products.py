import requests
from bs4 import BeautifulSoup as bs
import json
import csv

url = "https://flipkart.com/search?q="
# query to search for.
q = input("Enter a query: ")
file_name = q.replace(" ", "_")
# response recieved in bytes
resp = requests.get(url+q)
# parsing response content using BeautifulSoup class, so that we can perform operations on it.
parsed_html = bs(resp.content, 'html.parser')
# data cleaning
raw_data = parsed_html.find("script", attrs={"id":"is_script"})
data = raw_data.contents[0].replace("window.__INITIAL_STATE__ = ","").replace(";","")
json_data = json.loads(data)
req_data = json_data["pageDataV4"]["page"]["data"]["10003"]   #[10]["widget"]["data"]["products"][3]["productInfo"]
#req_json_data = json_data["seoMeta"]["answerBox"]["data"]["renderableComponents"][0]["value"]["data"]

data_list = []
# print(len(req_data))
try:
    for i in range(1, len(req_data)):
        d = {}
        jd = req_data[i]["widget"]["data"]["products"]
        # print(len(jd))
        # print("i: ", i, end="\n")
        for j in range(len(jd)):
            jd2 = jd[j]["productInfo"]["value"]
            
            d["title"] = jd2["titles"]["title"]
            d["keySpecs"] = jd2["keySpecs"]
            d["rating"] = jd2["rating"]["average"]
            d["ratingCount"] = jd2["rating"]["count"]
            d["price"] = jd2["pricing"]["finalPrice"]["value"]
            d["warranty"] = jd2["warrantySummary"]
            d["url"] = jd2["smartUrl"]

            # You can uncomment below lines if you want to print json output on terminal
            
            # print("Title: ",jd2["titles"]["title"],end="\n")
            # print("key specs: ", jd2["keySpecs"], end="\n")
            # print("Rating: ", jd2["rating"]["average"], end="\n")
            # print("Total ratings: ", jd2["rating"]["count"], end="\n")
            # print("Price: ", jd2["pricing"]["finalPrice"]["value"],end="\n")
            # print("warranty: ", jd2["warrantySummary"], end="\n")
            # print("Smart url: ", jd2["smartUrl"], end="\n")
        data_list.append(d)
            
            
except:
    pass 
# dumping data to result.json file
with open(file_name+'.json', 'w') as fp:
     json.dump(data_list, fp)

# Now let us write our data to csv file
data_file = open(file_name+'.csv', 'w') 
  
# create the csv writer object 
csv_writer = csv.writer(data_file) 
  
# Counter variable used for writing  
# headers to the CSV file 
count = 0
  
for data in data_list:
    if count == 0: 
  
        # Writing headers of CSV file 
        header = data.keys() 
        csv_writer.writerow(header) 
        count += 1
  
    # Writing data of CSV file 
    csv_writer.writerow(data.values()) 
  
data_file.close()