from main import db, app #, Pokemon
import csv
f = open('pokemon.csv', 'r')
reader = csv.reader(infile, delimiter = ",")
values = next(reader)
print(values)

db.create_all(app=app)



# add code to parse csv, create and save pokemon objects

# replace any null values with None to avoid db errors
