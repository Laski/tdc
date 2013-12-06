from BeautifulSoup import BeautifulSoup, SoupStrainer
import sys
print sys.stdout.encoding

import re
from mechanize import Browser

f=open("ips2", "r")
br = Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

for line in f:
	url="http://www.geoiptool.com/es/?IP="+line
	print url
	response=br.open(url)
	data = response.read() 
	for item in data.split("\n"):
		if "flag" in item and "class" in item:		
			print item