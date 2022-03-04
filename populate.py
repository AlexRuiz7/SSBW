# populate.py
from io import BytesIO

import requests
from mongoengine import connect
from PIL import Image

from models import Address, Person
# ======================================= #
# Constants
# ======================================= #
QUANTITY = 5
FAKER_API_URL = f'https://fakerapi.it/api/v1/persons?_quantity={QUANTITY}'
BASE_IMG_DIR = './imgs/'

# ======================================= #
# Connect to the DB
# ======================================= #
connect('fantasmas_ciberneticos', host='mongo')

# ======================================= #
# Populate the DB
# ======================================= #
def store_image(image_url: str, image_name: str) -> str:
    '''
    Downloads an image, stores it at the BASE_IMG_DIR with the given name and 
    returns its path.
    '''
    image_path = BASE_IMG_DIR + image_name + '.png'
    raw_image = requests.get(image_url).content
    i = Image.open(BytesIO(raw_image))
    i.save(image_path)
    return image_path


# Fetch data from the API
response = requests.get(FAKER_API_URL)

# Bulk insert the data as objects.
if (response.status_code == 200):
    data: list = response.json()['data']

    # Prepare the data
    bulk_data = []
    for item in data:
        # Create a new address
        address = item['address']
        new_address = Address(
            street          = address['street'],
            street_name     = address['streetName'],
            building_number = address['buildingNumber'],
            city            = address['city'],
            zipcode         = address['zipcode'],
            country         = address['country'],
            county_code     = address['county_code'],
            coordinates     = (address['latitude'], address['longitude'])
        )

        # Create a new person. Dooes not add an user image yet.
        new_person = Person(
            firstname = item['firstname'],
            lastname  = item['lastname'],
            email     = item['email'],
            phone     = item['phone'],
            birthday  = item['birthday'],
            gender    = item['gender'],
            address   = new_address,
            website   = item['website']
        )

        # Download, store and save reference to the user's image.
        new_person.image = store_image(item['image'], str(item['email']))

        # Push the new data to the bulk list
        bulk_data.append(new_person)

    # Insert the bulk data in the DB
    Person.objects.insert(bulk_data)
    print("Data inserted successfully")
else:
    raise requests.exceptions.HTTPError(
        f'Requests to {FAKER_API_URL} failed: {response.status_code}'
    )
