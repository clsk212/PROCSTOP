from transformers import pipeline
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from dateparser.search import search_dates
from langdetect import detect
import spacy

# Load models once to avoid reloading
nlp_en = spacy.load("en_core_web_sm")
nlp_es = spacy.load("es_core_news_sm")
intent_pipeline = pipeline("text-classification", model="facebook/bart-large-mnli")
sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def detect_intent(text):
    intent = intent_pipeline(text)[0]
    return intent['label'], intent['score']

def detect_topics(texts, num_topics=3):
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(texts)
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=0)
    lda.fit(X)
    topics = lda.transform(X)
    
    topic_labels = ["Topic " + str(i+1) for i in range(num_topics)]
    clustered_texts = {label: [] for label in topic_labels}
    for i, topic in enumerate(topics):
        topic_label = topic_labels[topic.argmax()]
        clustered_texts[topic_label].append(texts[i])
    
    return clustered_texts

def extract_entities(text, language="EN"):
    if language.upper() == 'EN':
        nlp = nlp_en
    elif language.upper() == 'ES':
        nlp = nlp_es
    else:
        raise ValueError("Unsupported language")

    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Additional date parsing for Spanish using dateparser
    if language == 'es':
        dates = search_dates(text, languages=[language.lower()])
        if dates:
            for date_text, date in dates:
                entities.append((date_text, 'DATE'))

    return entities

def process_text(text,language='ES'):
    print(text)

    # Extract entities
    entities = extract_entities(text, language.lower())

    # Detect intent
    intent_label, intent_score = detect_intent(text)

    # Print results
    print(f"Detected Language: {language}")
    print(f"Extracted Entities: {entities}")
    print(f"Detected Intent: {intent_label} (confidence: {intent_score:.2f})")

# User inputs
input1 = "Hi! Book a flight from New York to San Francisco next Monday, please Carmen."
input2 = "Un compañero del trabajo (Cristian) es malo conmigo y me hace estar triste en Getafe. A veces siento que es mi culpa, pero el no se preocupa por los demás. Lo bueno es que el 13 de Agosto se va de la empresa"

process_text(input1, 'en')
process_text(input2, 'es')

# Detect topics for a mixed batch of texts
texts = [
    "Book a flight from New York to San Francisco next Monday.",
    "What are the shipping options?",
    "Tell me about customer support.",
    "I'm really frustrated with your service.",
    "Reserva un vuelo de Nueva York a San Francisco el próximo lunes.",
    "¿Cuáles son las opciones de envío?",
    "Háblame del servicio al cliente.",
    "Estoy muy frustrado con tu servicio."
]

topics = detect_topics(texts, num_topics=2)
for i, topic in enumerate(topics):
    print(f"\nTopic {i+1}: {topic}")
