import requests
from bs4 import BeautifulSoup
import json

def GetSoup(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

data = {}

for i in range(2):  # Lặp qua 2 trang
    url = f"https://dangcongsan.vn/tu-tuong-van-hoa/p{i}"
    soup = GetSoup(url)
    articles = soup.find_all('div', class_='col-md-4 subnews-item')

    for idx, article in enumerate(articles, start=1):
        try:
            title = article.find('a')['title']
            link = article.find('a')['href']
            summary = article.find('div', class_='summary')
            content = summary.text.strip() if summary else None

            data[f"Article_{i * len(articles) + idx}"] = {
                'Title': title,
                'Content': content,
                'url': link
            }
        except Exception as e:
            print(f"Error: {e}")

# Lưu dữ liệu vào tệp JSON
with open('dcs_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Data saved to 'dcs_data.json' file.")
