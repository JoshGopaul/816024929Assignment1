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
def read_pokemon():

   with open("./pokemon.csv", 'r') as file:
     data = csv.reader(file)
     next(data)
     for column in data:
         name=column[30]
         attack=column[19]
         defense=column[25]
         hp=column[28]
         height=column[27]
         sp_attack=column[33]
         sp_defense=column[34]
         speed=column[35] 
         type1=column[36] 
         type2=column[37]

         if type2 == '':
            type2 = 'None'

         newpokemon = Pokemon(name=name, attack=attack, defense=defense, hp=hp, height=height, sp_attack=sp_attack, sp_defense=sp_defense,speed=speed, type1=type1, type2=type2)
         db.session.add(newpokemon)
         db.session.commit()      


@app.cli.command('list-pokemon', help = 'list Pokemon from pokemon.csv')
def list_pokemon():
      pokemon = Pokemon.query.all()
      print(pokemon)