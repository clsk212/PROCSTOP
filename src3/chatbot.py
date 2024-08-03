import argparse
from datetime import datetime
from constants import *
from feature_extraction.text_features import *
import random
import uuid

from database import mongo_query, save_message, create_user, save_to_conver

def presentation():
    print('\n\n\n\nPROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-')
    print('\nPROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-')
    print('\n                Welcome to PROCSTOP, your favourite activity recomendator!!!.')
    print('(                Anytime you want to exit just write "bye")')
    print('\n>>> Please choose a language: english (EN) or spanish (ES)')
    language = input('Yo: ')
    if language.upper() == 'ES':
        print('\n>>> Tienes ya tu cuenta?\n>>> Por favor escribe tu username. Si no tienes escribe "new".')
    else:
        print('\n>>> Do you have an account? \n>>> Please write your user id. If not, write "new".')
    user = input('Yo: ')
    if user.lower() == 'new':
        create_user(language)
    print('\n>>> Select the session mode: text (1), audio (2), video (3) or user settings (4)')
    session_mode = input('Yo: ')
    return language, user, session_mode

def intro(language, username):
    """
    Generate a personalized introduction for a user with language and user id asigned.
    """
    name = mongo_query('find_one','users',{'user_id': username},{'name': 1, '_id': 0})

    hour = datetime.now().hour
    if hour > 5 and hour < 13:
        moment = 'morning'
    elif hour >= 13 and hour < 20:
        moment = 'afternoon'
    else:
        moment = 'night'
    
    # Selección aleatoria de una introducción del momento y idioma seleccionado
    intros = {
        'EN': {
            'morning': [
                f'Good Morning, {name}. How do you feel today?',
                f"It's nice to see you again, {name}. How can I help you?",
                f"Hey {name}! Ready for the day?",
                f"Welcome!! It's always a pleasure to see you. How are you dude?",
                f"Top of the morning to you, {name}!",
                f"Morning, {name}! Let's make today great!"
            ],
            'afternoon': [
                f'Good afternoon, {name}. How can I assist you today?',
                f"It's nice to see you again, {name}. How can I help you?",
                f"Hey {name}! Did you have a good morning?",
                f"Good to see you this afternoon, {name}. What can I do for you?"
            ],
            'night': [
                f"Good night, {name}. How was your day? Wanna stop for a minute and observe yourself a little?",
                f"What a good night to see you, {name}",
                f"Hello {name}, how was your evening?",
                f"Good evening, {name}. How can I help you tonight?"
            ]
        },
        'ES': {
            'morning': [
                f'Buenos días, {name}. ¿Cómo te sientes hoy?',
                f'Es un placer verte de nuevo, {name}. ¿Cómo puedo ayudarte?',
                f'¡Hola {name}! ¿Listo para el día?',
                f'¡Bienvenido! Siempre es un placer verte. ¿Cómo estás, amigo?',
                f'¡Buenos días {name}!',
                f'¡Mañana, {name}! ¡Hagamos que hoy sea grandioso!'
            ],
            'afternoon': [
                f'Buenas tardes, {name}. ¿Cómo puedo asistirte hoy?',
                f'Es un placer verte de nuevo, {name}. ¿Cómo puedo ayudarte?',
                f'¡Hola {name}! ¿Tuviste una buena mañana?',
                f'Buenas tardes {name}. ¿En qué puedo ayudarte?'
            ],
            'night': [
                f'Buenas noches, {name}. ¿Cómo fue tu día? ¿Quieres detenerte un minuto y observarte un poco?',
                f'Qué buena noche para verte, {name}',
                f'Hola {name}, ¿cómo estuvo tu noche?',
                f'Buenas noches, {name}. ¿Cómo puedo ayudarte esta noche?'
            ]
        }
    }
    intro_selected = random.choice(intros[language.upper()][moment])
    
    print('\nPROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-')
    print('\nPROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-PROCSTOP-')
    print('\n\n\n\n>>> ' + intro_selected)
    return moment, name

def start_conversation(user_id):
    """Start a new conversation."""
    conver_id = str(uuid.uuid4())
    start_date = datetime.now()

    mongo_query('insert_one', 'conversations', {
        "conver_id": conver_id,
        "user_id": user_id,
        "start_date": start_date,
        "end_date": None,
        "duration": None,
        "num_interactions": 0,
        "topics": [],
        "entities": [],
        "emotions": []
    })
    
    return conver_id

def end_conversation(conver_id, topics):
    """End the conversation and update its metadata."""
    end_date = datetime.now()

    # Obtener todos los mensajes de la conversación para recolectar entidades y emociones
    messages = mongo_query('find', 'messages', {"conver_id": conver_id})
    
    entities = []
    emotions = []
    for message in messages:
        entities.extend(message.get('entities', []))
        emotions.append(message.get('emotion'))

    # Calcular la duración de la conversación
    conversation = mongo_query('find_one', 'conversations', {"conver_id": conver_id})
    start_date = datetime.fromisoformat(conversation['start_date'])
    end_date_dt = datetime.fromisoformat(end_date)
    duration = (end_date_dt - start_date).seconds

    # Actualizar la conversación con los metadatos finales
    mongo_query('update_one', 'conversations', {
        'filter': {"conver_id": conver_id},
        'update': {
            "$set": {
                "end_date": end_date,
                "duration": duration,
                "topics": topics,
                "entities": list(set(entities)),  # Eliminar duplicados
                "emotions": list(set(emotions))  # Eliminar duplicados
            }
        }
    })

def get_bot_response(user_input):
    # Generar una respuesta del bot basada en el input del usuario
    return "This is a sample response."

def init_chatbot():
    """
    Initialize the chatbot and manage the conversation.
    """
    language, username, session_mode = presentation()
    moment, name = intro(language=language, username=username)

    if session_mode == "1":
        print(f'Session Mode - {session_mode}')

        # Iniciar una nueva conversación
        conver_id = start_conversation(username)

        while True:
            user_input = input('Yo:')

            if user_input.lower() == 'bye':
                print('Hasta pronto!')

                # Finalizar la conversación
                end_conversation(conver_id)
                break

            # Obtener metadatos del mensaje del usuario (emociones, intenciones, entidades, tópicos)
            user_entities = extract_entities(user_input, language)
            user_emotion = extract_emotions(user_input)
            user_intention = detect_intention(user_input)
            user_topics = extract_topics(user_input)

            # Guardar el mensaje del usuario
            save_message(conver_id, username, "bot", user_input, user_entities, user_emotion, user_intention, user_topics)

            # Obtener respuesta del bot
            bot_response = get_bot_response(user_input)

            # Obtener metadatos del mensaje del bot (emociones, intenciones, entidades, tópicos)
            bot_entities = detect_entities(bot_response)
            bot_emotion = extract_emotions(bot_response)
            bot_intention = detect_intention(bot_response)
            bot_topics = extract_topics(bot_response)

            # Guardar el mensaje del bot
            save_message(conver_id, "bot", username, bot_response, bot_entities, bot_emotion, bot_intention, bot_topics)

            # Mostrar la respuesta del bot
            print(f'Bot: {bot_response}')

        #     message_info={
        #     'message_id': '',
        #     'user_id': '',
        #     'conver_id': '',
        #     'user_input': '',
        #     'bot_answer': '',
        #     'entities': '',
        #     'intention': '',
        #     'emotion_vector': ''
        # }


    elif session_mode == "2":
        print(f'Session Mode - {session_mode}')
    elif session_mode == "3":
        print(f'Session Mode - {session_mode}')
    elif session_mode == "4":
        print('Settings')
    else:
        print("Modo no válido. Terminando la sesión.")
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="chatbot",
        description="Initialize and execute chatbot",
    )

init_chatbot()