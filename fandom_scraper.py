import requests
from bs4 import BeautifulSoup
import textwrap

def scrape_fandom_character(anime, character):
    #Scrape fandom wiki.. need to know a fix for lesser known anime
    url = f"https://{anime}.fandom.com/wiki/{character.replace(' ', '_')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Probeer de naam van het karakter te vinden
        title = soup.find("h1").text.strip() if soup.find("h1") else character

        # Pak de eerste paragrafen met de beschrijving
        paragraphs = soup.find_all("p")
        character_description = "\n".join([p.text.strip() for p in paragraphs if len(p.text.strip()) > 100])
        
        # Splits de tekst in kleinere stukken (voor ChromaDB) -> ngo uitleg vragen
        chunks = textwrap.wrap(character_description, 512)

        return {"title": title, "chunks": chunks}
    else:
        return {"error": "Kan de pagina niet scrapen."}

# testing! (works) 
character_info = scrape_fandom_character("bts", "v")
print(character_info)

print()
