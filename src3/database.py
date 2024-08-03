import argparse
from pymongo import MongoClient
from cryptography.fernet import Fernet
from datetime import datetime
import uuid

# Configuration
key = Fernet.generate_key()
cif = Fernet(key)

class MongoConnection:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="procstop"):
        self.uri = uri
        self.db_name = db_name

    def __enter__(self):
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

def create_collection(name):
    """Cretate collection in Mongo 
    """
    with MongoConnection() as db:
        if name not in db.list_collection_names():
            db.create_collection(name)

def encrypt(datos):
    """Encrypt data for Mongo
    """
    return cif.encrypt(datos.encode())

def unencrypt(encrypted_data):
    """Unencrypt data from Mongo
    """
    return cif.decrypt(encrypted_data).decode()

def create_user(language):
    """
    Create a new user profile.
    """
    language = language.upper()
    creation = {
        'ES': [
            'Vamos a crear juntos tu perfil. \n>>> Lo primero de todo, ¿Cómo te gusta que te llamen? ',
            'Por favor completa los siguientes datos ',
            '- Nombre de usuario: ',
            '- Contraseña: ',
            '- Confirmar contraseña: ',
            '- Edad: ',
            '- Género: ',
            '- Ciudad: ',
            '- País: ',
            'Este nombre de usuario ya existe, por favor elige otro o añade caracteres.',
            'Las contraseñas no coinciden. Prueba de nuevo.',
            'Genial, ',
            '. Tu nuevo perfil se ha creado exitosamente!!'
        ],
        'EN': [
            "Let's create your account together. \n>>> First of all, how do you like to be called?",
            'Please complete the following required data, ',
            '- Username: ',
            '- Password: ',
            '- Confirm password: ',
            '- Age: ',
            '- Gender: ',
            '- City: ',
            '- Country: ',
            'This username already exists, please choose another or add some characters',
            "Passwords mismatched, try again.",
            'Nice, ',
            '. Your new profile has been created successfully!!'
        ]
    }

    print('\n>>> ' + creation[language][0])
    name = input('Yo: ')
    print('\n>>> '+ creation[language][1] + name + '.')
    username = input(creation[language][2])

    while mongo_query('find_one', 'user', {'user_id': username}):
        print('>>> ' + creation[language][9])
        username = input(creation[language][2])
        print('2')
    print('3')
    password = input(creation[language][3])
    conf_password = input(creation[language][4])

    while password != conf_password:
        print('4')
        print('>>> ' + creation[language][10])
        password = input(creation[language][3])
        conf_password = input(creation[language][4])

    user_info = {
        'user_id': username,
        'name': name,
        'age': input(creation[language][5]),
        'gender': input(creation[language][6]),
        'race': '',
        'language': language,
        'hobbies': [],
        'city': input(creation[language][7]),
        'country': input(creation[language][8]),
        'places': []
    }
    user_info['places'].append([user_info['city'], user_info['country']])
    save_user(user_info)
    print('\n>>> ' + creation[language][11] + name + creation[language][12])


def save_to_conver(conver_id, conver_info):
    """Save message to conversations

    Args:
        conver_id (str): Unique identifier of each conversation
        conver_info (dict): Dict with all necessary data
    """
    # Verificar si la conversación ya existe
    conver = mongo_query('find_one', 'conversations', {"conver_id": conver_id})

    if conver:
        # Preparar los campos de actualización
        update_fields = {
            "$push": {
                "messages": {
                    "user_id": conver_info["user_id"],
                    "message": conver_info["message"]
                }
            },
            "$set": {
                "topic": conver_info["topic"],
                "start_date": conver_info["start_date"],
                "end_date": conver_info["end_date"],
                "entities": conver_info["entities"],
                "intention_history": conver_info["intention"],
                "duration": conver_info["duration"]
            }
        }
        
        # Realizar la actualización
        mongo_query('update_one', 'conversations', {
            'filter': {"conver_id": conver_id},
            'update': update_fields
        })

    else:
        # Insertar una nueva conversación
        mongo_query('insert_one', 'conversations', {
            "conver_id": conver_id,
            "user_id": conver_info["user_id"],
            "topic": conver_info["topic"],
            "start_date": conver_info["start_date"],
            "end_date": conver_info["end_date"],
            "entities": conver_info["entities"],
            "intention_history": conver_info["intention"],
            "duration": conver_info["duration"],
            "messages": [{
                "user_id": conver_info["user_id"],
                "message": conver_info["message"]
            }]
        })

def save_message(conver_id, from_user, to_user, message, entities, emotion, intention, topics):
    """Save a message to MongoDB."""
    message_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    mongo_query('insert_one', 'messages', {
        "message_id": message_id,
        "conver_id": conver_id,
        "from": from_user,
        "to": to_user,
        "message": message,
        "timestamp": timestamp,
        "entities": entities,
        "emotion": emotion,
        "intention": intention,
        "topics": topics
    })
    
    # Actualizar el número de interacciones y los tópicos en la conversación
    mongo_query('update_one', 'conversations', {
        'filter': {"conver_id": conver_id},
        'update': {
            "$inc": {"num_interactions": 1},
            "$addToSet": {"topics": {"$each": topics}}
        }
    })

def save_user(user_info, new_hobby=None, new_person=None, new_place=None, new_name=None, new_age=None, new_language=None):
    """Save user personal information in MongoDB

    Args:
        user_info (dict): Dictionary with user information.
        new_hobby (str, optional): New hobby to add to the user's hobbies. Defaults to None.
        new_person (str, optional): New person to add to the user's people. Defaults to None.
        new_place (str, optional): New place to add to the user's places. Defaults to None.
        new_name (str, optional): New name to update the user's name. Defaults to None.
        new_age (int, optional): New age to update the user's age. Defaults to None.
        new_language (str, optional): New language to update the user's language. Defaults to None.
    """
    # Verify if user exists
    user = mongo_query('find_one', 'users', {"user_id": user_info['user_id']})
    
    if user:
        # Update user info
        update_fields = {}
        if new_hobby:
            update_fields.setdefault('$push', {}).setdefault('hobbies', new_hobby)
        if new_person:
            update_fields.setdefault('$push', {}).setdefault('people', new_person)
        if new_place:
            update_fields.setdefault('$push', {}).setdefault('places', new_place)
        if new_name:
            update_fields.setdefault('$set', {})['name'] = new_name
        if new_age is not None:
            update_fields.setdefault('$set', {})['age'] = new_age
        if new_language:
            update_fields.setdefault('$set', {})['language'] = new_language
        
        # Realizar la actualización si hay campos a actualizar
        if update_fields:
            mongo_query('update_one', 'users', {
                'filter': {"user_id": user_info['user_id']},
                'update': update_fields
            })

    else:
        # New user creation
        mongo_query('insert_one', 'users', {
            "user_id": user_info['user_id'],
            "name": user_info['name'],
            "age": user_info['age'],
            "gender": user_info['gender'],
            "race": user_info.get('race'),
            "language": user_info['language'],
            "hobbies": [new_hobby] if new_hobby else user_info.get('hobbies', []),
            "people": [new_person] if new_person else user_info.get('people', []),
            "places": [new_place] if new_place else user_info.get('places', [user_info.get('city'), user_info.get('country')])
        })

def mongo_query(query_type, collection_name, search_params, projection=None):
    """
    Execute queries in MongoDB.
    
    Args:
        query_type (str): The type of query ('find', 'find_one', 'insert_one', 'insert_many', 'update_one', 'update_many', 'delete_one', 'delete_many').
        collection_name (str): The name of the collection to query.
        search_params (dict): Dictionary with search, update, or insertion data according to the query type.
        projection (dict): Dictionary specifying the fields to include or exclude in the query result.
    
    Returns:
        result (list/dict): Result(s) of the query.
    """
    with MongoConnection() as db:
        collection = db[collection_name]

        # Dictionary of operations
        operations = {
            'find': lambda params: [doc for doc in collection.find(params, projection)],
            'find_one': lambda params: collection.find_one(params, projection),
            'insert_one': lambda params: collection.insert_one(params).inserted_id,
            'insert_many': lambda params: collection.insert_many(params).inserted_ids,
            'update_one': lambda params: collection.update_one(params['filter'], params['update']).modified_count,
            'update_many': lambda params: collection.update_many(params['filter'], params['update']).modified_count,
            'delete_one': lambda params: collection.delete_one(params).deleted_count,
            'delete_many': lambda params: collection.delete_many(params).deleted_count
        }
        
        # Execute the corresponding operation
        if query_type in operations:
            result = operations[query_type](search_params)
        else:
            raise ValueError("Unsupported query type.")
    
    return result
