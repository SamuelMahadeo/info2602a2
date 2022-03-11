from main import db, app, Pokemon
import csv
from os import path
file_path = path.abspath(__file__) # full path of your script
dir_path = path.dirname(file_path) # full path of the directory of your script
pokemon = path.join(dir_path,'pokemon.csv') # absolute zip file path

with open(pokemon, 'r') as infile:
    reader = csv.reader(infile, delimiter = ",")
    header = next(reader)
    for row in reader:
     pokemon = Pokemon(pid = row[32], name = row[30], attack = row[19], defense = row[25], hp = row[28],
     height = row[27], sp_attack = row[33], sp_defense = row[34], speed = row[35], type1= row[36], type2 = row[37], weight = row[38])
     print(pokemon.toDict())
     db.session.add(pokemon)
     db.session.commit()
    
db.create_all(app=app)



# add code to parse csv, create and save pokemon objects

# replace any null values with None to avoid db errors
