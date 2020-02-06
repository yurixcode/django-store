from enum import Enum

class OrderStatus(Enum): #Enum
    CREATED = 'CREATED'
    PAYED = 'PAYED'
    COMPLETED = 'COMPLETED' 
    CANCELED = 'CANCELED'

choices =[ (tag, tag.value) for tag in OrderStatus ]