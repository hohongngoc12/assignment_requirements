import requests
from bs4 import BeautifulSoup
import json
import re

def GetSoup(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def GetContent(url):
    try:
        print(f"Fetching content for URL: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')
            content_div = soup.find('div', class_='post-content')
            if content_div:
                text_content = content_div.get_text(separator='\n')
                # Clean up text content
                text_content = text_content.strip()
                text_content = re.sub(r'\n+', '\n', text_content)  # Remove excessive newline characters
                return text_content.strip()
            else:
                print(f"Content div not found for: {url}")
                return None
        else:
            print(f"Failed to fetch content for: {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching content for {url}: {e}")
        return None



data = {}

for i in range(5):  # Loop through the desired number of pages
    url = f"https://dangcongsan.vn/tu-tuong-van-hoa/p{i}"
    soup = GetSoup(url)
    articles = soup.find_all('div', class_='col-md-4 subnews-item')

    for idx, article in enumerate(articles, start=1):
        try:
            title = article.find('a')['title']
            link = article.find('a')['href']
            content = GetContent(link)

            data[f"Article_{i * len(articles) + idx}"] = {
                'Title': title,
                'Content': content,
                'url': link
            }
        except Exception as e:
            print(f"Error: {e}")

# Save data to a JSON file
with open('baodcs_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Data saved to 'baodcs_data.json' file.")
