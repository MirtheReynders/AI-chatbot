import requests
from bs4 import BeautifulSoup

def scrape(url):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # wattpad
        title = soup.find("h1").text.strip() if soup.find("h1") else "No title found"
        
        story_text = ""
        paragraphs = soup.find_all("p")
        for p in paragraphs:
            story_text += p.text + "\n"

        return {"title": title, "text": story_text[:2000]}  # add 2000 characters i think it needs more tbh
    else:
        return {"error": "no page."}

# testingk
# Works omg
url = "https://www.wattpad.com/14fdsdf7"
print(scrape(url))
