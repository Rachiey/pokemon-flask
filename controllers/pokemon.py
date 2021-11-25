''' pokemons controller '''
from werkzeug.exceptions import BadRequest

pokemons = [
    {'id': 1, 'name': 'Charizard', 'type': 'fire'},
    {'id': 2, 'name': 'Bulbasaur', 'type': 'grass'},
    {'id': 3, 'name': 'Squirtle', 'type': 'water'}
]

def index(req):
    return [p for p in pokemons], 200

def show(req, uid):
    return find_by_uid(uid), 200

def create(req):
    new_pokemon = req.get_json()
    new_pokemon['id'] = sorted([p['id'] for p in pokemon])[-1] + 1
    pokemons.append(new_pokemon)
    return new_pokemon, 201

def update(req, uid):
    pokemon = find_by_uid(uid)
    data = req.get_json()
    print(data)
    for key, val in data.items():
        pokemon[key] = val
    return pokemon, 200

def destroy(req, uid):
    pokemon = find_by_uid(uid)
    pokemons.remove(pokemon)
    return pokemon, 204

def find_by_uid(uid):
    try:
        return next(pokemon for pokemon in pokemons if pokemon['id'] == uid)
    except:
        raise BadRequest(f"We don't have that pokemon with id {uid}!")