from fandom_scraper import scrape_fandom_character
from llm_sorter import sort_character_info
from chroma_store import add_to_chroma

def load_character_data(anime, character):
    """Scrapet, sorteert en slaat karakterinformatie op in ChromaDB."""
    
    # Scrape de ruwe data
    fandom_data = scrape_fandom_character(anime, character)
    if "error" in fandom_data:
        print("❌ Kon Fandom niet scrapen.")
        return
    
    raw_text = fandom_data["raw_text"]
    
    # LLM gebruiken om de tekst te sorteren
    ## TODO DIT NIET DOEN
    sorted_data = sort_character_info(raw_text)
    
    # Opslaan in ChromaDB per categorie
    for category, text in sorted_data.items():
        if text:  # Alleen opslaan als er data is
            add_to_chroma(f"{character}_{category}", [text])

    print(f"✅ {character} informatie gesorteerd en opgeslagen in ChromaDB!")

# Test met een karakter
# load_character_data("naruto", "naruto uzumaki")

