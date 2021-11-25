from flask import Flask, jsonify, request
from flask_cors import CORS
from controllers import pokemon
from werkzeug import exceptions

server = Flask(__name__)
CORS(server)

@server.route('/')
def home():
    return jsonify({'message': 'Hello from our Pokemon!'}), 200

@server.route('/pokemon', methods=['GET', 'POST'])
def pokemons_handler():
    fns = {
        'GET': pokemon.index,
        'POST': pokemon.create
    }
    resp, code = fns[request.method](request)
    return jsonify(resp), code

@server.route('/pokemon/<int:pokemon_id>', methods=['GET', 'PATCH', 'PUT', 'DELETE'])
def pokemon_handler(pokemon_id):
    fns = {
        'GET': pokemon.show,
        'PATCH': pokemon.update,
        'PUT': pokemon.update,
        'DELETE': pokemon.destroy
    }
    resp, code = fns[request.method](request, pokemon_id)
    return jsonify(resp), code

@server.errorhandler(exceptions.NotFound)
def handle_404(err):
    return {'message': f'Oops! {err}'}, 404

@server.errorhandler(exceptions.BadRequest)
def handle_400(err):
    return {'message': f'Oops! {err}'}, 400

@server.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return {'message': f"It's not you, it's us"}, 500

if __name__ == "__main__":
    server.run(debug=True)