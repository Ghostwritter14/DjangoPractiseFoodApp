# Create your tests here.
import base64
import io
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from food.models import Item, CustomCombo, Category
from orders.models import Order, OrderItem

class OrdersViewsTestCase(TestCase):
    def setUp(self):
        # Create a user and log in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')

        # Create a category and two items
        self.cat = Category.objects.create(name='TestCat', slug='testcat')
        self.item1 = Item.objects.create(
            item_name='One', item_description='Desc1',
            item_price=3.00, item_image='url1', category=self.cat
        )
        self.item2 = Item.objects.create(
            item_name='Two', item_description='Desc2',
            item_price=4.50, item_image='url2', category=self.cat
        )

        # Create a combo for this user
        self.combo = CustomCombo.objects.create(user=self.user, name='MyCombo')
        self.combo.items.set([self.item1, self.item2])

    def test_add_to_cart_and_cart_detail(self):
        # add item1
        resp = self.client.post(reverse('orders:add_to_cart', args=[self.item1.id]), HTTP_REFERER='/food/')
        self.assertRedirects(resp, '/food/')
        session = self.client.session
        self.assertEqual(session['cart'][str(self.item1.id)], 1)

        # view cart
        resp = self.client.get(reverse('orders:cart_detail'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Your Cart')
        # item1 details present
        self.assertContains(resp, self.item1.item_name)
        self.assertContains(resp, '£3.0')

    def test_add_combo_to_cart(self):
        # add combo
        resp = self.client.post(reverse('orders:add_combo_to_cart', args=[self.combo.id]), HTTP_REFERER='/profile/')
        self.assertRedirects(resp, '/profile/')
        session = self.client.session
        # both items present
        self.assertEqual(session['cart'][str(self.item1.id)], 1)
        self.assertEqual(session['cart'][str(self.item2.id)], 1)

    def test_remove_from_cart(self):
        # preload cart
        session = self.client.session
        session['cart'] = {str(self.item1.id): 2, str(self.item2.id): 1}
        session.save()

        resp = self.client.post(reverse('orders:remove_from_cart', args=[self.item1.id]))
        self.assertRedirects(resp, reverse('orders:cart_detail'))
        session = self.client.session
        self.assertNotIn(str(self.item1.id), session['cart'])
        self.assertIn(str(self.item2.id), session['cart'])

    def test_checkout_and_order_detail(self):
        # preload cart
        session = self.client.session
        session['cart'] = {str(self.item1.id): 2, str(self.item2.id): 1}
        session.save()

        # checkout
        resp = self.client.post(reverse('orders:checkout'))
        # should redirect to order detail
        order = Order.objects.get(user=self.user)
        self.assertRedirects(resp, reverse('orders:detail', args=[order.id]))

        # confirm order items
        items = list(order.items.all())
        self.assertEqual(len(items), 2 + 1)  # two of item1, one of item2
        quantities = {oi.item.id: oi.quantity for oi in items}
        self.assertEqual(quantities[self.item1.id], 2)
        self.assertEqual(quantities[self.item2.id], 1)

        # session cart cleared
        self.assertEqual(self.client.session.get('cart', {}), {})

        # view order detail
        resp = self.client.get(reverse('orders:detail', args=[order.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, f"Order #{order.id}")
        self.assertContains(resp, self.item1.item_name)
        self.assertContains(resp, self.item2.item_name)

    def test_invoice_view_renders_qr(self):
        # create an order directly
        order = Order.objects.create(user=self.user)
        OrderItem.objects.create(order=order, item=self.item1, quantity=1)
        # call invoice
        resp = self.client.get(reverse('orders:invoice', args=[order.id]))
        self.assertEqual(resp.status_code, 200)
        # expect data:image/png;base64 in response
        self.assertContains(resp, 'data:image/png;base64')
        # basic check: QR code length
        content = resp.content.decode()
        self.assertTrue(len(content.split('data:image/png;base64,')[1]) > 50)
