import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama

# init the colorama module
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

# Source :
# https://thepythoncode.com/article/extract-all-website-links-python

def get_all_website_links(url,choice="all"):
	"""
	Returns all URLs that is found on `url` in which it belongs to the same website
	"""

	urls = set()
	internal_urls = set()
	external_urls = set()

	# domain name of the URL without the protocol
	domain_name = urlparse(url).netloc
	try :
		soup = BeautifulSoup(requests.get(url).content, "html.parser")
	except :
		raise ValueError("Problem with URL")
	
	for a_tag in soup.findAll("a"):
		href = a_tag.attrs.get("href")
		href = urljoin(url, href)
		parsed_href = urlparse(href)
		# remove URL GET parameters, URL fragments, etc.
		href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
		if domain_name not in href:
			# external link
			if href not in external_urls:
				print(f"{GRAY}[!] External link: {href}{RESET}")
				external_urls.add(href)
		elif href not in internal_urls:
			print(f"{GREEN}[*] Internal link: {href}{RESET}")
			internal_urls.add(href)
		urls.add(href)
	if choice=="all":
		return url
	elif choice=="intern":
		print(internal_urls)
		return internal_urls
	elif choice=="extern":
		return external_urls
	else :
		raise ValueError("Choice must be \"all\", \"intern\" or \"extern\"")
	
def filter(urls):
	filtered = set()
	filters = ["Category","Wikipedia","ISBN","Special","File"]
	for url in urls :
		ok = True
		for filter in filters :
			if filter in url :
				ok = False
				break
		if ok :
			filtered.add(url)
		
	return filtered

# number of urls visited so far will be stored here
total_urls_visited = 0

def crawl(url, max_urls):
	"""
	Crawls a web page and extracts all links.
	You'll find all links in `external_urls` and `internal_urls` global set variables.
	params:
		max_urls (int): number of max urls to crawl, default is 30.
	"""
	global total_urls_visited
	total_urls_visited += 1
	print(f"{YELLOW}[*] Crawling: {url}{RESET}")
	links = get_all_website_links(url,"intern")
	for link in links:
		if total_urls_visited > max_urls:
			break
		crawl(link, max_urls=max_urls)

if __name__ == "__main__":
	max_urls=30
	urls = get_all_website_links("https://en.wikipedia.org/wiki/Second_War_of_Scottish_Independence","intern")
	
	furls = filter(urls)
	for i in furls :
		print(i)
	print(len(urls))
	print(len(furls))

	#crawl("https://en.wikipedia.org/wiki/Second_War_of_Scottish_Independence",max_urls)

