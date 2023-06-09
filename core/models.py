from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(verbose_name="Nom du produit",
                            max_length=100, unique=True)
    brands = models.CharField(verbose_name="Marques du produit",
                              max_length=100)
    link = models.URLField(unique=True)
    nutriscore = models.CharField(max_length=1)
    image = models.URLField()
    fat = models.FloatField()
    saturated_fat = models.FloatField()
    sugars = models.FloatField()
    salt = models.FloatField()

    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = "Produits"
        ordering = ['name']

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    products = models.ManyToManyField(Product, related_name='categories')

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = "Catégories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='users')
    sub = models.ForeignKey(Product, on_delete=models.CASCADE,
                            related_name='subs')
    prod = models.ForeignKey(Product, on_delete=models.CASCADE,
                             related_name='prods')

    def __str__(self):
        return str(self.sub) + " remplace : " + str(self.prod) \
               + " sauvegardé par : " \
               + str(self.user)

    class Meta:
        verbose_name = "Favori"
        verbose_name_plural = "Favoris"
        ordering = ['user']