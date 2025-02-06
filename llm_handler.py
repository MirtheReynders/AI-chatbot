import ollama
from chroma_store import search_chroma

def generate_character_response(conversation_history, character, anime):
    """Laat AI antwoorden met alle context + volledige gespreksgeschiedenis."""
    ## TODO scraper apart maken voor de anime die je meegeeft
    # Zoek alle contextstukken per categorie uit ChromaDB
    ## TODO deze handmatig vullen bliep bloep
    categories = ["Appearance", "Personality", "Relationships", "Abilities"]
    all_context = []

    for category in categories:
        search_query = f"{character}_{category}"
        category_info = search_chroma(search_query, top_k=3)  # Meerdere stukken ophalen
        all_context.extend(category_info)  # Voeg alle gevonden contexten toe

    # Combineer alle context in een nette prompt
    character_context = "\n\n".join(all_context) if all_context else "Geen karakterinfo gevonden."
    ## TODO dit leuker aanpassen
    format = "context from surroundings /n character response"
    # **Volledige prompt met geheugen en karakterinfo**
    prompt = f"""
    You are roleplaying as {character} from {anime}. 
    Use the following information to stay in character and remember user details:

    **Character Context from ChromaDB:**  
    {character_context}

    **Conversation History (User Memory):**  
    {conversation_history}

    **User's latest message:**  
    {conversation_history.splitlines()[-1]}

    **Answer as {character}:**  

    **Answer in short turn based answers in this format: {format}**
    """

    response = ollama.chat(model="llama2", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]
