from bs4 import BeautifulSoup
import requests
categories=[
      "production-strategy",
      "catering-design",
      "event-tech-virtual",
      "venues-destinations",
      "meetings-trade-shows"
]
with open('bizBashLinks.txt', 'w') as file:
    for category in categories:
        url = f"https://www.bizbash.com/{category}"
        response = requests.get(url)
        s = BeautifulSoup(response.text, "html.parser")
        if response.status_code == 200:
                pagination=s.select_one(".pagination-controls__pages")
                paginationText=pagination.get_text().split(" ")
                numberOfPages=paginationText[3]
                # print(numberOfPages)
        for pageNum in range(int(numberOfPages)):
                print(pageNum, category)
                url = f"https://www.bizbash.com/{category}?page={pageNum}"
                response = requests.get(url)
                s = BeautifulSoup(response.text, "html.parser")
                if response.status_code == 200:
                    posts_elements = s.find_all( class_="section-feed-content-node__content-short-name")
                for element in posts_elements:
                    post_url = element.find("a")["href"]
                    file.write("https://www.bizbash.com"+post_url + '\n')                
        else:
                print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

