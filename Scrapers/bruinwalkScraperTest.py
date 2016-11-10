import urllib
import re

urls = ["http://www.bruinwalk.com", "http://google.com"]
i=0
regex = '<title>(.+?)</title>'
pattern = re.compile(regex)
while i<len(urls):
	htmlfile = urllib.urlopen(urls[i])
	htmltext = htmlfile.read()
	title = re.findall(pattern, htmltext)
	print title
	i+=1