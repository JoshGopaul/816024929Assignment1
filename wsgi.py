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