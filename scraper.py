import requests
from bs4 import BeautifulSoup
from time import sleep
from csv import DictWriter


def get_soup(url):
    """
        returns soup
    """
    res = requests.get(url)
    print(f"In process for \"{url}\"")
    return BeautifulSoup(res.text, "html.parser")


base_url = "http://quotes.toscrape.com"
soup = get_soup(base_url)
quotes_list = list()
queue = list()
queue.append(soup)

while len(queue) > 0:
    s = queue.pop(0)
    quotes = s.body.select(".quote")
    for quote in quotes:
        text = quote.select_one(".text").get_text()
        author = quote.select_one(".author").get_text()
        link = quote.select_one("a")["href"]
        s2 = get_soup(base_url + link)
        birth = s2.select_one(".author-born-date").get_text()
        location = s2.select_one(".author-born-location").get_text()
        quotes_list.append({
            "text": text,
            "author": author,
            "link": link,
            "birth": birth,
            "location": location
        })
    n = s.body.select_one("li.next > a")
    if n:
        # timed break to avoid instant req
        sleep(1)
        s = get_soup(base_url + n["href"])
        queue.append(s)
    else:
        print("Completed")

with open("quotes.csv", "w") as file:
    headers = quotes_list[0].keys()
    csv_writer = DictWriter(file, fieldnames=headers)
    csv_writer.writeheader()
    for q in quotes_list:
        csv_writer.writerow(q)





# <div class="quote" itemscope="" itemtype="http://schema.org/CreativeWork">
# <span class="text" itemprop="text">“It is our choices, Harry, that show what we truly are, far more than our abilities.”</span>
# <span>by <small class="author" itemprop="author">J.K. Rowling</small>
# <a href="/author/J-K-Rowling">(about)</a>
# </span>
# <div class="tags">
#             Tags:
#             <meta class="keywords" content="abilities,choices" itemprop="keywords"/>
#<a class="tag" href="/tag/abilities/page/1/">abilities</a>
#<a class="tag" href="/tag/choices/page/1/">choices</a>
#</div>
#</div>

