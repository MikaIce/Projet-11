""" This file contains all Tests about Product app """
from django.test import TestCase
from django.urls import reverse
from .models import Category, Product, Favorite, User
from .views import redirect
from io import StringIO
from django.core.management import call_command


class TestProduct(TestCase):
    """Test all Product app views"""

    def setUp(self):
        """Creating objects for tests"""
        user = User.objects.create(username='name',
                                   password='abdcef123')
        cat = Category.objects.create(name='name')
        prod = Product.objects.create(name='name',
                                      brands='brand',
                                      link='http://url.com',
                                      nutriscore='B',
                                      image='http://imageurl.com',
                                      fat=1,
                                      saturated_fat=1,
                                      sugars=1,
                                      salt=1)

        sub = Product.objects.create(name='nametest',
                                     brands='testbrand',
                                     link='http://testurl.com',
                                     nutriscore='A',
                                     image='http://testimageurl.com',
                                     fat=0,
                                     saturated_fat=0,
                                     sugars=0,
                                     salt=0)
        cat.products.add(prod)
        cat.products.add(sub)
        cat.save()
        Favorite.objects.create(user_id=user.id,
                                sub_id=sub.id,
                                prod_id=prod.id)

    def test_no_search_view(self):
        response = self.client.get(reverse('core:search'))
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed(redirect('index.html'))

    def test_bad_search_view(self):
        response = self.client.get(reverse('core:search'), {
            'query': 'no_products'})
        self.assertEquals(response.status_code, 302,
                          "Nous n'avons trouvé aucun produit "
                          "correspondant à votre recherche")
        self.assertTemplateUsed(redirect('index.html'))

    def test_good_search_view(self):
        response = self.client.get(reverse('core:search'), {'query': 'name'})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/search.html')

    def test_product_view(self):
        prod_id = Product.objects.first().id
        response = self.client.get(reverse('core:product',
                                           args=[prod_id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/product.html')

    def test_substitute_view(self):
        sub_id = Product.objects.last().id
        response = self.client.get(reverse('core:substitute',
                                           args=[sub_id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'substitute.html')

    def test_save_logged_in_view(self):
        user = User.objects.first()
        self.client.force_login(user)
        prod = Product.objects.first().id
        sub_id = Product.objects.last().id
        response = self.client.get(reverse('core:save',
                                           args=[prod, sub_id]))
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed(redirect('index.html'))

    def test_save_already_saved_view(self):
        user = User.objects.first()
        self.client.force_login(user)
        prod_id = Product.objects.first().id
        sub_id = Product.objects.last().id
        response = self.client.get(reverse(
            'core:save', args=[sub_id, prod_id]))
        self.assertEqual(response.status_code, 302,
                         'Le produit est déjà sauvegardé')
        self.assertTemplateUsed(redirect('index.html'))

    def test_favorite_logged_in_view(self):
        user = User.objects.first()
        self.client.force_login(user)
        response = self.client.get(reverse('core:favorite'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'favorite.html')

    def test_delete_logged_in_view(self):
        user = User.objects.first()
        self.client.force_login(user)
        fav = Favorite.objects.first().id
        response = self.client.get(reverse('core:delete',
                                           args=[fav]))
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed(redirect('index.html'))

    def test_save_logged_out_view(self):
        """When user is not logged in"""
        prod = Product.objects.first().id
        sub_id = Product.objects.last().id
        response = self.client.get(reverse('core:save',
                                           args=[prod, sub_id]))
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed(redirect('users/login.html'))

    def test_favorite_logged_out_view(self):
        """When user is not logged in"""
        response = self.client.get(reverse('core:favorite'))
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed(redirect('users/login.html'))

    def test_delete_logged_out_view(self):
        """When user is not logged in"""
        fav = Favorite.objects.first().id
        response = self.client.get(reverse('core:delete',
                                           args=[fav]))
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed(redirect('users/login.html'))

    def test_cat_string(self):
        cat = Category.objects.first()
        self.assertEqual(str(cat), 'name')

    def test_prod_string(self):
        prod = Product.objects.first()
        self.assertEqual(str(prod), 'name')

    def test_sub_string(self):
        sub = Favorite.objects.first()
        self.assertEqual(str(sub),
                         'nametest remplace : name sauvegardé par : name')


class TestFillDatabase(TestCase):
    def test_fill_database(self):
        out = StringIO()
        call_command('fill_database', stdout=out)
        self.assertIn('Base de données remplie avec succès', out.getvalue())