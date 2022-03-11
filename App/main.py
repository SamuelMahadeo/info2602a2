import json
from flask import Flask, request, render_template
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 

from models import db , User, Pokemon, MyPokemon

''' Begin boilerplate code '''
def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
  app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7) 
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()


''' End Boilerplate Code '''

''' Set up JWT here '''
def authenticate(uname, password):
  user = User.query.filter_by(username=uname).first()
  if user and user.check_password(password):
    return user

def identity(payload):
  return User.query.get(payload['identity'])

jwt = JWT(app, authenticate, identity)
''' End JWT Setup '''

# edit to query 50 pokemon objects and send to template
@app.route('/')
def index():
  pokemon = Pokemon.query.offset(0).limit(50).all()
  return render_template('index.html', pokemon = pokemon)

@app.route('/pokemon', methods = ['GET'])
def getpokemon():
  pokemon = Pokemon.query.all()
  pokemon = [poke.toDict() for poke in pokemon]
  return json.dumps(pokemon)

@app.route('/signup', methods = ['POST'])
def signup():
  userdata = request.get_json()
  newuser = User(username = userdata['username'], email = userdata['email'])
  newuser.set_password(userdata['password'])
  try:
   db.session.add(newuser)
   db.session.commit()
  except IntegrityError:
    db.session.rollback()
    return('username or email already exists')
  return('user created')
  

@app.route('/mypokemon', methods =['POST'])
@jwt_required()
def mypokemon():
  pokedata = request.get_json()
  pokemon = Pokemon.query.get(pokedata['pid'])
  newpokemon = MyPokemon(id = current_identity.id, pid = pokedata['pid'], 
                name = pokedata['name'], pokemon = pokemon)
  db.session.add(newpokemon)
  db.session.commit()
  return (pokedata['name'] + ' captured')

@app.route('/mypokemon', methods = ['GET'])
@jwt_required()
def getMyPokemon():
  myPokemon = MyPokemon.query.all()
  myPokemon = [poke.toDict() for poke in myPokemon]
  return json.dumps(myPokemon)

@app.route('/mypokemon/<id>', methods = ['GET'])
@jwt_required()
def getOnePokemon(id):
   numPokemon = MyPokemon.query.all()
   if len(numPokemon) == 0:
     return 'No pokemon captured'
   mypokemon = MyPokemon.query.filter_by(id = current_identity.id, bid = id).first()
   if mypokemon == None:
     return 'id out of range'
   return json.dumps(mypokemon.toDict())

@app.route('/mypokemon/<id>', methods =['PUT'])
@jwt_required()
def putPokemon(id):
  newName = request.get_json()
  mypokemon = MyPokemon.query.all()
  location = int(id) -1
  poke = mypokemon[location]
  if poke == None:
    return 'No pokemon found at that id'
  poke.name = newName['name']
  db.session.add(poke)
  db.session.commit()
  return('Updated'), 201
 


@app.route('/mypokemon/<id>', methods = ['DELETE'])
@jwt_required()
def deletePokemon(id):
  mypokemon = MyPokemon.query.all()
  location = int(id) -1
  poke = mypokemon[location]
  if poke == None:
    return ('invalid id'), 204
  db.session.delete(poke)
  db.session.commit()
  return ('pokemon deleted'), 204

@app.route('/app')
def client_app():
  return app.send_static_file('app.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)