import ollama

##TODO DIT HOEFT NIET VGM
def sort_character_info(raw_text):
    """Laat een LLM de gescrapte tekst sorteren in categorieën."""
    
    prompt = f"""
    Je bent een assistent die informatie over een fictief personage organiseert. 
    Sorteer de volgende tekst in de categorieën:

    - **Appearance** (fysiek uiterlijk en kleding)
    - **Personality** (gedrag, karaktereigenschappen)
    - **Relationships** (vrienden, vijanden, connecties)
    - **Abilities** (speciale krachten, vechtstijl, skills)
    
    Als er geen informatie is over een categorie, laat die dan leeg.

    Hier is de ruwe tekst:
    
    {raw_text}

    Geef het resultaat terug in JSON-formaat:
    {{
      "Appearance": "...",
      "Personality": "...",
      "Relationships": "...",
      "Abilities": "..."
    }}
    """

    response = ollama.chat(model="llama2", messages=[{"role": "user", "content": prompt}])
    
    # Extract JSON data uit het AI-antwoord
    import json
    try:
        structured_data = json.loads(response["message"]["content"])
    except json.JSONDecodeError:
        structured_data = {"Appearance": "", "Personality": "", "Relationships": "", "Abilities": ""}

    return structured_data
