# models.py

from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField, StringField, EmailField 
from mongoengine.fields import URLField, IntField, LongField, GeoPointField, DateTimeField


class Address(EmbeddedDocument):
    '''
    Address model. Embedded Document of the Person model.
    '''
    street          = StringField()
    street_name     = StringField()
    building_number = IntField()
    city            = StringField()
    zipcode         = IntField()
    country         = StringField(max_length=60)
    county_code     = StringField(max_length=3)
    coordinates     = GeoPointField()


class Person(Document):
    '''
    Person Mmdel.
    '''
    firstname = StringField(max_length=60, required=True)
    lastname  = StringField(max_length=60, required=True)
    email     = EmailField()
    phone     = LongField()
    birthday  = DateTimeField()
    gender    = StringField(choices=['male', 'female'])
    address   = EmbeddedDocumentField(Address)
    website   = URLField()
    image     = URLField()
