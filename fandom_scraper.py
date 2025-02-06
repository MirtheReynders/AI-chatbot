import requests
from bs4 import BeautifulSoup

##TODO HANDMATIG SORTEN
def scrape_fandom_character(anime, character):
    """Scrapet ruwe tekst van een Fandom wiki-pagina."""
    url = f"https://{anime}.fandom.com/wiki/{character.replace(' ', '_').title()}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1").text.strip() if soup.find("h1") else character

        # Pak alle paragrafen samen
        paragraphs = [p.text.strip() for p in soup.find_all("p") if len(p.text.strip()) > 100]
        raw_text = "\n\n".join(paragraphs)  # Maak een enkele string van de tekst

        return {"title": title, "raw_text": raw_text}
    
    else:
        return {"error": "Kan de pagina niet scrapen."}

# testing! (works) 
character_info = scrape_fandom_character("bungostraydogs", "osamu dazai")
print(character_info)

print()
