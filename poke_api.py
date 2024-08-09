'''
Library for interacting with the PokeAPI.
https://pokeapi.co/
'''
import requests
import os

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():
    # Test out the functions
    poke_info = get_pokemon_info("rockruff")
    all_pokemon = get_all_pokemon_names()
    if all_pokemon:
        print(f"Total Pokémon names retrieved: {len(all_pokemon)}")
    image_dir = r'C:\temp\pokemon_images'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    download_pokemon_artwork("rockruff", image_dir)
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
        return None

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
        return None

def get_all_pokemon_names():
    """Fetches a list of all Pokemon names from the PokeAPI.

    Returns:
        list: List of Pokemon names, if successful. Otherwise None.
    """
    url = POKE_API_URL + "?limit=10000"
    print(f'Fetching all Pokemon names...', end='')
    resp_msg = requests.get(url)

    if resp_msg.status_code == requests.codes.ok:
        print('success')
        all_pokemon = resp_msg.json().get('results', [])
        return [pokemon['name'] for pokemon in all_pokemon]
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return None

def download_pokemon_artwork(pokemon, save_dir):
    """Downloads and saves the official artwork for a specified Pokemon.

    Args:
        pokemon (str): Pokemon name (or Pokedex number)
        save_dir (str): Directory to save the artwork image

    Returns:
        bool: True, if successful. False, if unsuccessful.
    """
    pokemon_info = get_pokemon_info(pokemon)
    if not pokemon_info:
        return False

    # Get the artwork URL
    artwork_url = pokemon_info['sprites']['other']['official-artwork']['front_default']
    if not artwork_url:
        print(f"No artwork found for {pokemon.capitalize()}.")
        return False

    # Download the artwork
    print(f"Downloading artwork for {pokemon.capitalize()}...", end='')
    resp_msg = requests.get(artwork_url)

    if resp_msg.status_code == requests.codes.ok:
        print('success')
        # Save the image
        image_data = resp_msg.content
        image_path = os.path.join(save_dir, f"{pokemon.lower()}.png")
        try:
            with open(image_path, 'wb') as file:
                file.write(image_data)
            print(f"Artwork saved to {image_path}")
            return True
        except Exception as e:
            print(f"failure: {e}")
            return False
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return False

if __name__ == '__main__':
    main()
