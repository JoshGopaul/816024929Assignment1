from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
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
   user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False) #fk
   pokemon_id = db.Column(db.Integer, db.ForeignKey('Pokemon.id'), nullable=False)#fk
   name = db.Column(db.String(80), unique=True, nullable=False)

   def __init__(self, name):
       self.name = name


   def get_json(self):
      return {
        "id": self.id,
        "name": self.name
      }
   

class Pokemon(db.Model):
   id = db.Column(db.Integer, primary_key=True) 
   name = db.Column(db.String(80), unique=True, nullable=False)
   attack = db.Column(db.Integer)
   defense = db.Column(db.Integer)
   hp = db.Column(db.Integer)
   height = db.Column(db.Integer)
   sp_attack = db.Column(db.Integer)
   sp_defense = db.Column(db.Integer)
   speed = db.Column(db.Integer)
   type1 = db.Column(db.String(80), unique=True, nullable=False)
   type2 = db.Column(db.String(80), unique=True, nullable=False)

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
        "speed": self.sp_speed,
        "type1": self.type1,
        "type2": self.type2
      }