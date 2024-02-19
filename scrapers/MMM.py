from bs4 import BeautifulSoup 
import requests 
from collections import deque

urls = set()
files = set()

def getLinks(site):
	with open('myMM.txt', 'w') as file:
		queue = deque([site])
		while queue:
			current_site = queue.popleft()
			try:
				r = requests.get(current_site)
				s = BeautifulSoup(r.text, "html.parser")
				for i in s.find_all("a"):
					flag=0
					try:
						href = i.attrs['href']
						if href.startswith("/"):
							new_site = site + href
							flag=1
						elif href.startswith("https://mymodernmet.com"):
							new_site=href
							flag=1
						if href not in files and flag==1 and href.find("/pages")==-1 and href.find("/author")==-1 and href.find("protection#")==-1:
								files.add(href)
								urls.add(new_site)
								print(new_site)
								file.write(new_site+"\n")
								queue.append(new_site)
								
					except:
						continue

			except:
				pass

		return urls

if __name__ == "__main__":
		start_site = "https://www.thisiscolossal.com"
		getLinks(start_site)
