import os
import spacy
from fuzzywuzzy import process
from collections import OrderedDict

# Load SpaCy large model
nlp = spacy.load("en_core_web_lg")

# Predefined CDP-related topics for comparison
CDP_TOPICS = [
    "customer data platform", "CDP integration", "event tracking", 
    "user profiles", "data pipeline", "identity resolution", 
    "consent management", "data synchronization", "real-time personalization"
]

# Hardcoded list of unrelated topics (will be **strictly rejected**)
NON_CDP_TOPICS = [
    "movie", "film", "cinema", "actor", "actress", "director",
    "sports", "football", "basketball", "cricket", "weather",
    "date", "time", "politics", "government", "president", "prime minister",
    "healthcare", "medicine", "covid", "pandemic"
]

def is_relevant_query(query):
    """
    Checks if a query is related to CDP topics.
    - **Strictly rejects non-CDP queries**.
    - Uses **NLP similarity** with a threshold (0.5) for CDP relevance.
    """
    query_lower = query.lower()

    # Hard Reject Any Query That Mentions a Non-CDP Topic**
    if any(topic in query_lower for topic in NON_CDP_TOPICS):
        return False  

    # Check similarity with **CDP-related topics**
    query_doc = nlp(query_lower)
    max_similarity = max(query_doc.similarity(nlp(topic)) for topic in CDP_TOPICS)

    return max_similarity >= 0.5  # Must be at least **50% similarity** to CDP topics

def preprocess_query(query):
    """Preprocess query using spaCy."""
    doc = nlp(query)
    processed_query = " ".join([sent.text for sent in doc.sents])
    return processed_query[:300]  # Limit to 300 characters for better results

def filter_relevant_text(lines):
    """Filters out irrelevant lines and focuses on step-by-step instructions."""
    include_keywords = [
        "how to", "steps", "guide", "configure", "build", "create",
        "setup", "process", "step", "click", "select", "go to", "API", "integration"
    ]
    exclude_keywords = NON_CDP_TOPICS  # Use same hard-rejection list

    filtered_lines = []
    for line in lines:
        lower_line = line.lower()
        if any(word in lower_line for word in include_keywords) and not any(bad_word in lower_line for bad_word in exclude_keywords):
            filtered_lines.append(line)

    return filtered_lines

def search_documentation(cdp_name, query):
    """
    Searches documentation with improved ranking and filters irrelevant questions.
    """
    # **Reject non-CDP questions first**
    if not is_relevant_query(query):
        return ["❌ This chatbot only answers Customer Data Platform (CDP)-related questions. Please ask a relevant question."]

    file_path = f"data/{cdp_name}.txt"
    if not os.path.exists(file_path):
        return [f"⚠️ Documentation for {cdp_name} is not available. Run the scraper first."]

    query = preprocess_query(query)

    # Load text
    with open(file_path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]
    
    lines = filter_relevant_text(lines)

    if not lines:
        return ["⚠️ No relevant setup instructions found. Try refining your query."]

    # Fuzzy match top 20 results
    best_matches = process.extract(query, lines, limit=20)

    # Convert query to NLP doc
    query_doc = nlp(query)

    # Rank by NLP similarity (ignore empty vectors)
    ranked_results = sorted(
        best_matches, 
        key=lambda match: query_doc.similarity(nlp(match[0])) if nlp(match[0]).vector_norm else 0, 
        reverse=True
    )

    # Remove duplicates while keeping order
    final_results = list(OrderedDict.fromkeys([match[0] for match in ranked_results]))

    return final_results[:5] if final_results else ["⚠️ No relevant setup instructions found."]

# Example usage:
if __name__ == "__main__":
    print(search_documentation("mparticle", "How can I create a user profile in mParticle?"))
    print(search_documentation("segment", "How do I set up a new source in Segment?"))
    print(search_documentation("lytics", "How do I build an audience segment in Lytics?"))
    print(search_documentation("zeotap", "How can I integrate my data with Zeotap?"))
    print(search_documentation("segment", "Which movie is getting released this week?")) 
    print(search_documentation("segment", "What is the weather today?"))  
