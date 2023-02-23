from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random
db = SQLAlchemy()



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    

    def __init__(self, username, email, password):
       self.username = username
       self.email = email
       self.set_password(password)
    
    
    def get_json(self):
      return {
        "id": self.id,
        "username": self.username,
        "email": self.email,
        "password": self.password
      }


    def catch_pokemon(self, pokemon_id, name):
       new_pokemon = Pokemon.query.filter_by(id=pokemon_id).first()
       if new_pokemon:
          user_pokemon = UserPokemon(user_id=self.id,pokemon_id=pokemon_id,name=name,species=new_pokemon.name)
          db.session.add(user_pokemon)
          db.session.commit()
          return user_pokemon
       else:
          return None
    
    def release_pokemon(self, pokemon_id, name):
        my_pokemon = UserPokemon.query.filter_by(id=pokemon_id, user_id=self.id).first()
        if my_pokemon:
           db.session.delete(my_pokemon)
           db.session.commit()
           return True
        return None  
    
    def rename_pokemon(self, pokemon_id, name):
       my_pokemon = UserPokemon.query.filter_by(id=pokemon_id, user_id=self.id).first()
       if my_pokemon:
          my_pokemon.name = name
          db.session.add(my_pokemon)
          db.session.commit()
          return my_pokemon
       return None

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    

    def __repr__(self):
        return f'<User {self.username} - {self.email}>'
    
    





class UserPokemon(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #fk
   pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)#fk
   name = db.Column(db.String(80), nullable=False)
   species = db.Column(db.String(80), nullable=False)

   def __init__(self, user_id, pokemon_id, name, species):
       self.name = name
       self.user_id = user_id
       self.pokemon_id = pokemon_id
       self.species = species

   def get_json(self):
      return {
        "id": self.id,
        "user_id": self.user_id,
        "pokemon_id":self.pokemon_id,
        "name": self.name,
        "species": self.species
      }

   def __repr__(self):
    return f'<Pokemon: {self.id} | Poke Index ID: {self.pokemon_id} | Pokemon Name:{self.name} | User ID: {self.user_id}>'  


class Pokemon(db.Model):
   id = db.Column(db.Integer, primary_key=True) 
   name = db.Column(db.String(80), nullable=False)
   attack = db.Column(db.Integer)
   defense = db.Column(db.Integer)
   hp = db.Column(db.Integer)
   height = db.Column(db.Integer)
   sp_attack = db.Column(db.Integer)
   sp_defense = db.Column(db.Integer)
   speed = db.Column(db.Integer)
   type1 = db.Column(db.String(80))
   type2 = db.Column(db.String(80))

   def __init__(self, name, attack, defense, hp, height, sp_attack, sp_defense, speed, type1, type2):
       self.name = name
       self.attack = attack
       self.defense = defense
       self.hp = hp
       self.height = height
       self.sp_attack = sp_attack
       self.sp_defense = sp_defense
       self.speed = speed
       self.type1 = type1
       self.type2 = type2

   def get_json(self):
      return {
        "id": self.id,
        "name": self.name,
        "attack": self.attack,
        "defense": self.defense,
        "hp": self.hp,
        "height": self.height,
        "sp_attack": self.sp_attack,
        "sp_defense": self.sp_defense,
        "speed": self.speed,
        "type1": self.type1,
        "type2": self.type2
      }

   def __repr__(self):
        return f'<Pokemon ID: {self.id} - Pokemon Name:{self.name} - Attack:{self.attack} - Defense:{self.defense} - HP:{self.hp} - Height:{self.height} - Special Attack:{self.sp_attack} - Special Defense:{self.sp_defense} - Speed:{self.speed} - Type 1:{self.type1} - Type 2:{self.type2} > \n'