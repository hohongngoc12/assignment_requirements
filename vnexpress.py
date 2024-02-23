import requests
from bs4 import BeautifulSoup
import json

def GetSoup(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

data = {}

for i in range(50):  # Lặp qua 50 trang
    url = f"https://vnexpress.net/phap-luat/ho-so-pha-an-p{i}"
    soup = GetSoup(url)
    descriptions = soup.find_all('p', class_='description')
    
    for idx, desc in enumerate(descriptions, start=1):
        try:
            title = desc.a['title']
            content = desc.a.text.strip()
            url = desc.a['href']
            
            data[f"Article_{idx}"] = {
                'title': title,
                'content': content,
                'url': url
            }
        except Exception as e:
            print(f"Error: {e}")

# Ghi dữ liệu vào tệp JSON
with open('vnexpress_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Data saved to 'vnexpress_data.json' file.")