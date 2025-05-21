# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Item, Category

class FoodViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user and log in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')

        # Create a Category
        self.cat = Category.objects.create(name='TestCat', slug='testcat')

        # Create two Items
        self.item1 = Item.objects.create(
            item_name='Item One',
            item_description='First item',
            item_price=9.99,
            item_image='http://example.com/img1.png',
            category=self.cat,
            ingredients='ing1,ing2'
        )
        self.item2 = Item.objects.create(
            item_name='Item Two',
            item_description='Second item',
            item_price=4.50,
            item_image='http://example.com/img2.png',
            category=self.cat,
            ingredients=''
        )

    def test_landing_page(self):
        url = reverse('landing')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/landing.html')

    def test_index_view_lists_items(self):
        url = reverse('food:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # both items present in context
        self.assertIn(self.item1, response.context['item_list'])
        self.assertIn(self.item2, response.context['item_list'])
        self.assertTemplateUsed(response, 'food/index.html')

    def test_detail_view_shows_ingredients_list(self):
        url = reverse('food:detail', args=[self.item1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # ingredients_list created by splitting
        self.assertEqual(response.context['ingredients_list'], ['ing1','ing2'])
        self.assertTemplateUsed(response, 'food/detail.html')

    def test_category_view_filters(self):
        url = reverse('food:category', args=[self.cat.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # both items share the same category
        self.assertQuerysetEqual(
            response.context['item_list'],
            map(repr, [self.item1, self.item2]),
            ordered=False
        )
        self.assertContains(response, self.cat.name)

    def test_create_item_view_get_and_post(self):
        url = reverse('food:create_item')
        # GET shows the form
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/item_form.html')

        # POST creates a new item
        new_data = {
            'item_name': 'New Item',
            'item_description': 'Desc',
            'item_price': '5.00',
            'item_image': 'http://example.com/new.png',
            'category': self.cat.pk,
            'ingredients': 'a,b'
        }
        response = self.client.post(url, new_data)
        # should redirect to detail of the new object
        self.assertEqual(response.status_code, 302)
        new = Item.objects.get(item_name='New Item')
        self.assertRedirects(response,
            reverse('food:detail', args=[new.pk])
        )

    def test_edit_item_view_get_and_post(self):
        url = reverse('food:edit_item', args=[self.item1.pk])
        # GET pre-fills the form
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Item One')

        # POST updates description
        data = {
            'item_name': 'Item One',
            'item_description': 'Updated',
            'item_price': '9.99',
            'item_image': self.item1.item_image,
            'category': self.cat.pk,
            'ingredients': 'ing1,ing2'
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('food:detail', args=[self.item1.pk]))
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.item_description, 'Updated')

    def test_delete_item_view_get_and_post(self):
        url = reverse('food:delete_item', args=[self.item2.pk])
        # GET shows confirmation
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/item_delete.html')

        # POST deletes and redirects to index
        response = self.client.post(url)
        self.assertRedirects(response, reverse('food:index'))
        with self.assertRaises(Item.DoesNotExist):
            Item.objects.get(pk=self.item2.pk)
