import os
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

def user_login(username, password):
  user = RegularUser.query.filter_by(username=username).first()
  if user and user.check_password(password):
    return create_access_token(identity=username)
  return None

  
@app.route('/login', methods=['POST'])
def user_login_view():
  data = request.json
  token = user_login(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  return jsonify(access_token=token)


@app.route('/signup', methods=['POST'])
def signup_user_view():
  data = request.json
  new_user = RegularUser(data['username'], data['email'], data['password'])

  #prevent regular user sharing username with admin
  admin = Admin.query.filter_by(username=data['username']).first()
  user = RegularUser.query.filter_by(username=data['username']).first()
  
  if admin or user:
    return jsonify(message='username already taken!'), 409
  
  db.session.add(new_user)
  db.session.commit()
  return jsonify(message=f'User {new_user.id} - {new_user.username} created!'), 201



if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)
