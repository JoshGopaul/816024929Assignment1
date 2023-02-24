## Josh Gopaul
## 816024929

import click
import csv
from tabulate import tabulate
from App import db, User, Pokemon, UserPokemon
from App import app

@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()
  print('database initialized')



@app.cli.command("create-user", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("email", default="robmail")
@click.argument("password", default="robpass")
def create_user_command(username, email, password):
  newuser = User(username, email, password)
  try:
    db.session.add(newuser)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    print(str(e))
    print(f'{username} already exists!')
  else:
    print(f'{username} created!')


@app.cli.command('get-users', help="Lists users in the app")
def list_users_command():
  users = User.query.all()
  print(users)

@app.cli.command('read-pokemon', help = 'Read Pokemon from pokemon.csv')
def read_pokemon_command():

   with open("./pokemon.csv", 'r') as file:
     data = csv.reader(file)
     next(data)
     for column in data:
         name=column[30]
         attack=column[19]
         defence=column[25]
         hp=column[28]
         height=column[27]
         weight=column[38]
         sp_attack=column[33]
         sp_defence=column[34]
         speed=column[35] 
         type1=column[36] 
         type2=column[37]

         if type2 == '':
            type2 = 'None'

         newpokemon = Pokemon(name=name, attack=attack, defence=defence, hp=hp, height=height, weight=weight, sp_attack=sp_attack, sp_defence=sp_defence,speed=speed, type1=type1, type2=type2)
         db.session.add(newpokemon)
         db.session.commit()      


@app.cli.command('list-pokemon', help = 'list Pokemon from pokemon.csv')
def list_pokemon_command():
      pokemon = Pokemon.query.all()
      print(pokemon)


@app.cli.command('catch-pokemon', help = 'adds a pokemon to your list')
@click.argument("user_id", default="1")
@click.argument("pokemon_id", default="801")
@click.argument("name", default="Joe")
def catch_pokemon_command(user_id,pokemon_id, name):
      user = User.query.filter_by(id=user_id).first()
      pokemon = Pokemon.query.filter_by(id=pokemon_id).first()
      if pokemon:
         my_pokemon = user.catch_pokemon(pokemon_id=pokemon_id,name=name)
         print(f'Pokemon {my_pokemon.id} - {my_pokemon.name} created!')
      else:
        print(f'{pokemon_id} is not a valid pokemon id!')

@app.cli.command('get-mypokemon', help = 'List your pokemon')
@click.argument("user_id", default="1")
@click.argument("pokemon_id",default="1")
def get_mypokemon_command(user_id, pokemon_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
       mypokemon = UserPokemon.query.filter_by(user_id=user_id,id=pokemon_id).first()
       print(mypokemon)
    else:
       print("Not Found!")
 

@app.cli.command('list-mypokemon', help = 'List your pokemon')
@click.argument("user_id", default="1")
def list_mypokemon_command(user_id):
    data =[]
    user = User.query.filter_by(id=user_id).first()
    if user:
        for my_pokemon in UserPokemon.query.filter_by(user_id=user_id).all():
            data.append([ my_pokemon.id, my_pokemon.pokemon_id, my_pokemon.name, my_pokemon.species, my_pokemon.user_id])
        print (tabulate(data, headers=["Pokemon ID", "Poke Index ID", "Pokemon Name", "Pokemon Species", "User ID"]))


@app.cli.command('release-mypokemon', help = 'List your pokemon')
@click.argument("user_id", default="1")
@click.argument("pokemon_id",default="4")
@click.argument("name", default="Kartana")
def release_mypokemon_command(user_id, pokemon_id, name):
    user = User.query.filter_by(id=user_id).first()
    if user:
       my_pokemon = UserPokemon.query.filter_by(user_id=user_id,id=pokemon_id).first()
       print(my_pokemon)
       my_pokemon_deleted = user.release_pokemon(pokemon_id=my_pokemon.id, name=my_pokemon.name)
       print("Pokemon Deleted")
    else:
       print("Not Found!")

@app.cli.command('rename-mypokemon', help = 'List your pokemon')
@click.argument("user_id", default="1")
@click.argument("pokemon_id",default="3")
@click.argument("name", default="jay")
def rename_mypokemon_command(user_id, pokemon_id, name):
    user = User.query.filter_by(id=user_id).first()
    if user:
       my_pokemon = UserPokemon.query.filter_by(user_id=user_id,id=pokemon_id).first()
       print(my_pokemon)
       my_pokemon = user.rename_pokemon(pokemon_id=my_pokemon.id, name=name)
       print("Pokemon Renamed")
    else:
       print("Not Found!")