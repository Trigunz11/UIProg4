import requests

BASE_URL = "https://swapi.dev/api"

def get_arid_planet_films():
    response = requests.get(f"{BASE_URL}/planets/")
    planet_count = 0
    arid_planet_films = set()

    while response.status_code == 200:
        data = response.json()
        for planet in data['results']:
            if 'arid' in planet['climate']:
                for film_url in planet['films']:
                    arid_planet_films.add(film_url)
        if data['next']:
            response = requests.get(data['next'])
        else:
            break

    return len(arid_planet_films)

def get_wookies_in_episode_6():
    film_id = 6  # The ID for "Episode VI: Return of the Jedi"
    response = requests.get(f"{BASE_URL}/films/{film_id}/")
    if response.status_code == 200:
        film_data = response.json()
        wookie_count = 0

        for character_url in film_data['characters']:
            character_response = requests.get(character_url)
            if character_response.status_code == 200:
                character_data = character_response.json()
                if character_data['species']:
                    species_response = requests.get(character_data['species'][0])
                    if species_response.status_code == 200:
                        species_data = species_response.json()
                        if species_data['name'] == 'Wookiee':
                            wookie_count += 1

        return wookie_count
    return 0

def get_largest_starship():
    response = requests.get(f"{BASE_URL}/starships/")
    max_length = 0
    largest_starship = None

    while response.status_code == 200:
        data = response.json()
        for starship in data['results']:
            try:
                length = float(starship['length'].replace(',', ''))
                if length > max_length:
                    max_length = length
                    largest_starship = starship['name']
            except ValueError:
                continue
        if data['next']:
            response = requests.get(data['next'])
        else:
            break

    return largest_starship

if __name__ == "__main__":
    # a) ¿En cuántas películas aparecen planetas cuyo clima sea árido?
    arid_planet_films_count = get_arid_planet_films()
    print(f"a) Planetas con clima árido aparecen en {arid_planet_films_count} películas.")

    # b) ¿Cuántos Wookies aparecen en la sexta película?
    wookies_count = get_wookies_in_episode_6()
    print(f"b) Hay {wookies_count} Wookies en la sexta película.")

    # c) ¿Cuál es el nombre de la aeronave más grande en toda la saga?
    largest_starship = get_largest_starship()
    print(f"c) La aeronave más grande en toda la saga es {largest_starship}.")






