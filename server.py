from flask import Flask, jsonify, request, url_for, render_template, redirect
from flask_cors import CORS
from controllers import pokemon
from werkzeug import exceptions
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

server = Flask(__name__)
server.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'
Bootstrap(server)
CORS(server)

class NameForm(FlaskForm):
    name = StringField('Which actor is your favorite?', validators=[DataRequired()])
    submit = SubmitField('Submit')

headings = ("Name", "Type")
data = [
    {'id': 1, 'name': 'Charizard', 'type': 'fire'},
    {'id': 2, 'name': 'Bulbasaur', 'type': 'grass'},
    {'id': 3, 'name': 'Squirtle', 'type': 'water'}
]

@server.route('/')
def home():
    
    form = NameForm()
    message = ""
    if form.validate_on_submit():
        name = form.name.data
        if name.lower() in data:
            # empty the form field
            form.name.data = ""
            id = data.id
            # redirect the browser to another route and template
            return redirect( url_for('pokemon', id=id) )
        else:
            message = "That actor is not in our database."
    return render_template('home.html', data=data, form=form, message=message)
    # return render_template("home.html", data=data, form = form )

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