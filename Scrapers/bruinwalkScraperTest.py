import urllib
import re
import cfscrape

#returns a CloudflareScraper instance
scraper = cfscrape.create_scraper() 
# htmltext = scraper.get("http://bruinwalk.com").content
# regex = '<title>(.+?)</title>'
# pattern = re.compile(regex)
# title = re.findall(pattern, htmltext)
# print title


#urlClasses = ["chem-184", "com-sci-130", "com-sci-131"]
urlClasses = ["a-o-sci-1", "i-a-std-1", "se-a-st-1", "a-o-sci-1l", "aero-st-a", "af-amer-m114c", "af-amer-m5", "afro-am-m150d", "an-n-ea-cm101b", "anthro-191ha", "anthro-m186", "appling-102w", "appling-155", "appling-c113", "arabic-105", "com-sci-131"]
i=0
# titleRegex = '<title>(.+?)</title>'
# titlePattern = re.compile(regex)
# while i<len(urlClasses):
# 	htmltext = scraper.get("http://bruinwalk.com/classes/" + urlClasses[i] + "/").content
# 	titles=re.findall(titlePattern, htmltext)
# 	print title
# 	i+=1

ratingRegEx = 'span class="rating">(.+?)</span>'
ratingPattern = re.compile(ratingRegEx)
titleRegex = '<title>(.+?)</title>'
titlePattern = re.compile(titleRegex)
while i<len(urlClasses):
	htmltext = scraper.get("http://bruinwalk.com/classes/" + urlClasses[i] + "/").content
 	title=re.findall(titlePattern, htmltext)
 	print title
	ratings=re.findall(ratingPattern, htmltext)
	classOverallAverage =0
	j=0
	if(len(ratings)==0):
		print "No Bruinwalk ratings for this class"
		i+=1
		continue
	while j<len(ratings):
		#print ratings[j]
		classOverallAverage += float(ratings[j])
		j+=1
	classOverallAverage /= len(ratings)
	print classOverallAverage
	i+=1

# urls = ["http://www.bruinwalk.com", "http://google.com"]
# i=0
# regex = '<title>(.+?)</title>'
# pattern = re.compile(regex)
# while i<len(urls):
# 	htmlfile = urllib.urlopen(urls[i])
# 	htmltext = htmlfile.read()
# 	title = re.findall(pattern, htmltext)
# 	print title
# 	i+=1
