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
data = raw_data.contents[0].strip().replace("window.__INITIAL_STATE__ = ","").replace(";","")
json_data = json.loads(data)
req_json_data = json_data["seoMeta"]["answerBox"]["data"]["renderableComponents"][0]["value"]["data"]

# dumping data to result.json file
with open(file_name+'.json', 'w') as fp:
     json.dump(req_json_data, fp)

# Now let us write our data to csv file
data_file = open(file_name+'.csv', 'w') 
  
# create the csv writer object 
csv_writer = csv.writer(data_file) 
  
# Counter variable used for writing  
# headers to the CSV file 
count = 0
  
for data in req_json_data: 
    if count == 0: 
  
        # Writing headers of CSV file 
        header = data.keys() 
        csv_writer.writerow(header) 
        count += 1
  
    # Writing data of CSV file 
    csv_writer.writerow(data.values()) 
  
data_file.close()