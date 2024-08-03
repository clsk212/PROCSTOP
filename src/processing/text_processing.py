
def tokenization(text):
    """
    Tokenization of a text"""

stopwords_list = set(stopwords.words('english'))

def remove_stopwords(txt):
    """Eliminación de stopwords en el idioma de un texto
    
    Args:
        txt (str): Texto input a limpiar
    """
    tokens = word_tokenize(txt)
    filtered_tokens = [w for w in tokens if w.lower() not in stopwords_list]
    return ' '.join(filtered_tokens)

def stopwords(dataset):
    """Eliminación de stopwords dentro de un registro del dataset
    
    Args:
        dataset (DatasetDict): Dataset a limpiar
    """
    dataset['premise'] = [remove_stopwords(text) for text in dataset['premise']]
    dataset['hypothesis'] = [remove_stopwords(text) for text in dataset['hypothesis']]
    return dataset

lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(word):
    """Mapeo de etiquetas POS
    
    Args:
        word (str): Palabra input de una frase a lematizar
    """
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def lemmatize_sentence(sentence):

    """Lematización de una frase
    
    Args:
        sentence (str): Frase input de un texto a lematizar
    """
    words = nltk.word_tokenize(sentence)
    lemmatized_words = [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in words]
    return ' '.join(lemmatized_words)

def tokenize_function(dataset):
    """Tokenize"""


def text_cleaning(text):
    """ Process text"""
    remove_stopwords(text)
    lemmatize_sentence(text)
    tokenize_function(text)
