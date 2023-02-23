import os
import csv
import wsgi
from datetime import timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from .models import db, User, UserPokemon, Pokemon


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'MySecretKey'
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
    CORS(app)
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()
jwt = JWTManager(app)  #setup flask jwt-e to work with app

@app.route('/')
def index():
  return '<h1>Poke API</h1>'

## User Creation - start
def user_login(username, password):
  user = User.query.filter_by(username=username).first()
  if user and user.check_password(password):
    return create_access_token(identity=username)
  return None

  
@app.route('/login', methods=['POST'])
def user_login_view():
  data = request.json
  token = user_login(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username/password given'), 401
  return jsonify(access_token=token)


@app.route('/signup', methods=['POST'])
def signup_user_view():
  data = request.json
  new_user = User(data['username'], data['email'], data['password'])

  #prevent regular user sharing username with admin
  #admin = Admin.query.filter_by(username=data['username']).first()
  user = User.query.filter_by(username=data['username']).first()
  
  if user:
    return jsonify(message='username or email already exists'), 400
  
  db.session.add(new_user)
  db.session.commit()
  return jsonify(message=f'{new_user.username} created'), 201

## User Creation - end

## Read and List Pokemon - start

@app.route('/pokemon', methods=['GET'])
def get_pokemonlist():
      pokemons = Pokemon.query.all()
      if pokemons:
         return jsonify([pokemon.get_json() for pokemon in pokemons]), 200
      else:
         return jsonify(message=f'Pokemon List Unavailable'), 400

@app.route('/mypokemon', methods=['GET'])
@jwt_required()
def get_mypokemonlist():
      username = get_jwt_identity()
      user = User.query.filter_by(username=username).first()
      pokemons = UserPokemon.query.filter_by(user_id=user.id)
      return jsonify([pokemon.get_json() for pokemon in pokemons])

@app.route('/mypokemon', methods=['POST'])
@jwt_required()
def save_pokemon():
      data = request.json
      username = get_jwt_identity()
      user = User.query.filter_by(username=username).first()
      pokemon = Pokemon.query.filter_by(id=data['pokemon_id']).first()
      if pokemon:
         my_pokemon = user.catch_pokemon(pokemon_id=data['pokemon_id'],name=data['name'])
         return jsonify(message = f'{my_pokemon.name} captured with id: {my_pokemon.id}'), 201
      else:
       id=data['pokemon_id']
       return jsonify(message = f'{id} is not a valid pokemon id'), 400

@app.route('/mypokemon/<int:id>', methods=['GET'])
@jwt_required()
def get_mypokemon(id):
      username = get_jwt_identity()
      user = User.query.filter_by(username=username).first()
      pokemon = UserPokemon.query.filter_by(user_id=user.id,id=id).first()
      if pokemon:
         return jsonify(message = f'id: {pokemon.id}, Name: {pokemon.name}, Species: {pokemon.species}'), 201
      else:
         return jsonify(message = f'id {id} does not belong to {user.username}'), 401


@app.route('/mypokemon/<int:id>', methods=['PUT'])
@jwt_required()
def rename_mypokemon(id):
      data = request.json
      username = get_jwt_identity()
      user = User.query.filter_by(username=username).first()
      pokemon = UserPokemon.query.filter_by(user_id=user.id, id=id).first()
      if pokemon:
         temp = pokemon.name
         pokemon = user.rename_pokemon(pokemon_id=id,name=data['name'])
         return jsonify(message = f'{temp} renamed to {pokemon.name}'), 201
      else:
         return jsonify(message = f'id {id} does not belong to {user.username}'), 401

@app.route('/mypokemon/<int:id>', methods=['DELETE'])
@jwt_required()
def release_mypokemon(id):
      username = get_jwt_identity()
      user = User.query.filter_by(username=username).first()
      pokemon = UserPokemon.query.filter_by(user_id=user.id, id=id).first()
      if pokemon:
         temp=pokemon.name
         pokemon = user.release_pokemon(pokemon_id=id, name=pokemon.name)
         return jsonify(message = f'{temp} released'), 200
      else:
         return jsonify(message = f'id {id} does not belong to {user.username}'), 401         

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)
