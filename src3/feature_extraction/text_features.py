import spacy
import dateparser

# Load spaCy English and Spanish models once
nlp_en = spacy.load("en_core_web_sm")
nlp_es = spacy.load("es_core_news_sm")

def extract_entities(text, language="en"):
    if language == "EN":
        doc = nlp_en(text)
    elif language == "ES":
        doc = nlp_es(text)
    else:
        return []

    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Additional date parsing for Spanish using dateparser
    if language == "es":
        dates = dateparser.search.search_dates(text, languages=['es'])
        if dates:
            for date_text, date in dates:
                entities.append((date_text, 'DATE'))
    return entities


def extract_emotions(text):
    """
    Extract emotions from the text using a Hugging Face model.

    Parameters:
    text (str): The text to analyze.

    Returns:
    list: A list of detected emotions.
    """
    emotion_classifier = pipeline('text-classification', model='j-hartmann/emotion-english-distilroberta-base', return_all_scores=True)
    emotions = emotion_classifier(text)
    
    # Extract emotions with scores above a certain threshold, e.g., 0.5
    threshold = 0.5
    extracted_emotions = [emotion['label'] for emotion in emotions[0] if emotion['score'] > threshold]
    
    return extracted_emotions

def detect_intention(text):
    # Detectar intención en el texto
    return "inform"

def extract_topics(text):
    # Extraer tópicos del texto
    return ["work", "gym"]

def text_feature_extraction(message):
    """
    Extract emotions, entities, and places from the message.

    Parameters:
    message (str): The text message to process.

    Returns:
    dict: A dictionary with extracted features.
    """
    # Extract features
    emotions = extract_emotions(message)
    entities = extract_entities(message)
    places = extract_places(message)

    # Return the extracted features
    return {
        'emotions': emotions,
        'entities': entities,
        'places': places
    }