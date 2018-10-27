
import requests,re,json,html2text
import time,urllib,pickle,urllib3
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

GID = raw_input("Group Id\t: ")
TOKEN = raw_input("Access Token\t: ")
LOG = raw_input("Log Name\t: ")

def loadfileurl(urlnya):
	session = requests.session()
	response = session.get(urlnya, allow_redirects=False)
	return response.content
  
def jsonreadku(teksny):
	j = json.loads(teksny);
	return j

def save_id(text):
	with open(LOG+'.txt', 'a') as fp:
		pickle.dump(text, fp)

def replace_string(text, target):
	string = open(LOG+'.txt').read()
	new_str = string.replace(text, target)
	open(LOG+'.txt', 'w').write(new_str)

def next_crawl_id(next_url):
	next_grab_api = loadfileurl(next_url)
	next_result_json = jsonreadku(next_grab_api)
	next_list_id = next_result_json['data']
	next_list_page = next_result_json['paging']
	for nli in next_list_id:
		save_id(nli['id'])
	if next_list_page.get('next') is not None:
		next_crawl_id(next_list_page.get('next'))

def crawl_id():
	grab_api = loadfileurl("https://graph.facebook.com/"+GID+"/members?fields=id&limit=5000&access_token="+TOKEN)
	result_json = jsonreadku(grab_api)
	list_id = result_json['data']
	list_page = result_json['paging']
	for li in list_id:
		save_id(li['id'])
	if list_page.get('next') is not None:
		next_crawl_id(list_page.get('next'))

def run():
	crawl_id()
	replace_string('V', '')
	replace_string('.V', '')
	replace_string('\np0', '')
	replace_string('.', '')
	print "Crawl Successfully!!!"
	
run()
