from django.db import models


# Create your models here.
class Palabra:
    def __init__(self, palabra, cantidad):
        self.palabra = palabra
        self.cantidad = cantidad

    def __repr__(self):
        return repr((self.palabra, self.cantidad))
