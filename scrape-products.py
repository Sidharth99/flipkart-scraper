import requests
from bs4 import BeautifulSoup as bs
import json

url = "https://flipkart.com/search?q="
q = input("Enter a query: ")
resp = requests.get(url+q)
parsed_html = bs(resp.content, 'html.parser')
data = parsed_html.find("script", attrs={"id":"is_script"})
j = data.contents[0].strip()
j = j.replace("window.__INITIAL_STATE__ = ","").replace(";","")
y = json.loads(j)
y = y["seoMeta"]["answerBox"]["data"]["renderableComponents"][0]["value"]["data"]
with open('result2.json', 'w') as fp:
     json.dump(y, fp)
