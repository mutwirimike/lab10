'''
Library for interacting with the PokeAPI.
https://pokeapi.co/
'''
import requests
import image_lib
import os

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():
    # Test out the get_pokemon_into() function
    # Use breakpoints to view returned dictionary
    poke_info = get_pokemon_info("Rockruff")

    get_pokemon_list()
    return

def get_pokemon_info(pokemon):
    """Gets information about a specified Pokemon from the PokeAPI.

    Args:
        pokemon (str): Pokemon name (or Pokedex number)

    Returns:
        dict: Dictionary of Pokemon information, if successful. Otherwise None.
    """
    # Clean the Pokemon name parameter by:
    # - Converting to a string object,
    # - Removing leading and trailing whitespace, and
    # - Converting to all lowercase letters
    pokemon = str(pokemon).strip().lower()

    # Check if Pokemon name is an empty string
    if pokemon == '':
        print('Error: No Pokemon name specified.')
        return

    # Send GET request for Pokemon info
    print(f'Getting information for {pokemon.capitalize()}...', end='')
    url = POKE_API_URL + pokemon
    resp_msg = requests.get(url)

    # Check if request was successful
    if resp_msg.status_code == requests.codes.ok:
        print('success')
        # Return dictionary of Pokemon info
        return resp_msg.json()
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')

    # TODO: Define function that gets a list of all Pokemon names from the PokeAPI

def get_pokemon_list(pokemon_limit='3000', offset='0'):
    """Get a list of all pokemon

    Args:
        pokemon_limit (str): Max number of pokemon to get in the list
    
    Returns:
        List of pokemon names  
    """
    print("Getting a list of Pokemon Names...")
    pokemon_list = []

    url = POKE_API_URL + f'?offset={offset}&limit={pokemon_limit}'
    
    re = requests.get(url)

    if re.status_code == requests.codes.ok:
        data = re.json()
        for item in data['results']:
            pokemon_list.append(item['name'])
    else:
        print('Failure')
        print(f'Response code: {re.status_code} ({re.reason})')

    return pokemon_list

    # TODO: Define function that downloads and saves Pokemon artwork

def download_artwork(pokemon_list, image_dir):
    """Download pokemon artwork from PokeAPI

    Args:
        pokemon_list (list): list of pokemon names    
        image_dir (str): image directory to save file to
    
    Returns:
        Nothing    
    """

    for item in pokemon_list:
        pokeInfo = get_pokemon_info(item)
        imageDir = os.path.join(image_dir, f'{pokeInfo['name']}.png')
        if os.path.exists(imageDir):
            print("FIle Already Saved!")
        else:
            imageURL = pokeInfo['sprites']['front_default']
            imageData = image_lib.download_image(imageURL)            
            image_lib.save_image_file(imageData, imageDir)
    return

if __name__ == '__main__':
    main()