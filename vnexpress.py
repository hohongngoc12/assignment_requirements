import requests
from bs4 import BeautifulSoup
import json

def GetSoup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def GetContent(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Identify the correct element containing the article content
            content_div = soup.find('article', class_='fck_detail')  # Update this with the correct class
            if content_div:
                # Extract text content
                text_content = content_div.get_text(separator='\n')
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

for i in range(2):  # Loop through the desired number of pages
    url = f"https://vnexpress.net/phap-luat/ho-so-pha-an-p{i}"
    soup = GetSoup(url)
    articles = soup.find_all('p', class_='description')

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
with open('hspa_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Data saved to 'hspa_data.json' file.")
