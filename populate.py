# populate.py
from mongoengine import connect, Document, EmbeddedDocument	
from mongoengine.fields import EmbeddedDocumentField, StringField, EmailField, URLField, FloatField, DateTimeField

import requests

connect('fantasmas_ciberneticos', host='mongo')


class Address(EmbeddedDocument):
  street          = StringField()
  street_name     = StringField()
  building_number = StringField()
  city            = StringField()
  zipcode         = StringField(max_length=60)
  country         = StringField(max_length=60)
  county_code     = StringField(max_length=3)
  latitude        = FloatField()
  longitude       = FloatField()

class Person(Document):
  firstname = StringField(max_length=60, required=True)
  lastname  = StringField(max_length=60, required=True)
  email     = EmailField()
  phone     = StringField()
  birthday  = DateTimeField()
  gender    = StringField(choices=['male', 'female'])
  address   = EmbeddedDocumentField(Address)
  website   = URLField()
  image     = URLField()


# Fetch data from the API
QUANTITY = 5
FAKER_API_URL = f'https://fakerapi.it/api/v1/persons?_quantity={QUANTITY}'
response = requests.get(FAKER_API_URL)

if (response.status_code == 200):
  data: list = response.json()['data']

  # Prepare the data
  bulk_data = []
  for item in data:
    # Create a new address
    new_address = Address(
      street          = item['address']['street'],
      street_name     = item['address']['streetName'],
      building_number = item['address']['buildingNumber'],
      city            = item['address']['city'],
      zipcode         = item['address']['zipcode'],
      country         = item['address']['country'],
      county_code     = item['address']['county_code'],
      latitude        = item['address']['latitude'],
      longitude       = item['address']['longitude']
    )
    # Create a new person
    new_person = Person(
      firstname = item['firstname'],
      lastname  = item['lastname'],
      email     = item['email'],
      phone     = item['phone'],
      birthday  = item['birthday'],
      gender    = item['gender'],
      address   = new_address,
      website   = item['website'],
      image     = item['image']
    )
    # Push the new data to the bulk list
    bulk_data.append(new_person)
  
  # Insert the bulk data in the DB
  Person.objects.insert(bulk_data)
  print("Data inserted successfully")
else:
  raise requests.exceptions.HTTPError(
    f'Requests to {FAKER_API_URL} failed: {response.status_code}'
  )