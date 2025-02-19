import requests
from bs4 import BeautifulSoup

def get_stock_news(ticker: str):
    """
    Fetches the latest news aritcles for a given stock ticker from Google news.
    """

    base_url = f"https://www.google.com/search?={ticker}+stock+news&tbm=nws"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(base_url, headers = headers)

    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("div", class_ = "SoaBEf")

    news_list = []

    for article in articles:
        title_tag = article.find("div", class_ = "n0jPhd ynAwRc MBeuO nDgy9d")
        if title_tag:
            title = title_tag.text.strip()
            link_tag = article.find("a")
            link = f"https://www.google.com{link_tag['href']}" if link_tag else None
            news_list.append({
                "title": title,
                "url": link
            })

    return news_list