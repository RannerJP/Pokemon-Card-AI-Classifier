from pokemontcgsdk import Card
from pokemontcgsdk import Type

from pokemontcgsdk import RestClient
import os
import requests
from datetime import datetime
start_time = datetime.now()
api_key = os.environ.get('POKEMON_TCG_API_KEY')
RestClient.configure(api_key)

types = Type.all()
types.append("Item") #In order to include item cards in sorting

for type in types:
    print(f"starting {type} folder")
    
    type_folder = os.path.join('.', type)
    os.makedirs(type_folder, exist_ok=True)

    cards = Card.where(q=f'types:{type}') if type != "Item" else Card.where(q=f'subtypes:Item')
    
    for card in cards:
        image_url = card.images.small
        
        set_name, set_number = os.path.split(os.path.dirname(image_url)), os.path.basename(image_url)
        set_and_number = set_name[1].replace('/', '') + set_number
        filename = os.path.join(type_folder, set_and_number)
        
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"File downloaded and saved to {filename} for {type} folder")
        else:
            print(f"Failed to download for Darkness. Status code: {response.status_code}")
print(f"Program started at {start_time}. Program ended at {datetime.now()}.")
