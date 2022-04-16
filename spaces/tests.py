from django.test   import TestCase, Client

from spaces.models import Space, Image, Category
from users.models import Host, User

class SpaceListViewTest(TestCase):
    def setUp(self):
        Category.objects.bulk_create([
            Category(id=1, title='title 1'),
            Category(id=2, title='title 2')
        ])
        User.objects.bulk_create([
            User(id=1, nickname='user1', email='user1@gmail.com', kakao_id=1111111111),
            User(id=2, nickname='user2', email='user2@gmail.com', kakao_id=2222222222)
        ])
        Host.objects.bulk_create([
            Host(id=1, user_id=1, phone_number='01000000000'),
            Host(id=2, user_id=2, phone_number='01099999999')
        ])
        Space.objects.bulk_create([
            Space(id=1, host_id=1, title='space title 1', sub_title='space sub title 1', room_name='room 1', detail='detail 1', max_capacity=10, address='address 1', price=1000, category_id=1),
            Space(id=2, host_id=2, title='space title 2', sub_title='space sub title 2', room_name='room 2', detail='detail 2', max_capacity=10, address='address 2', price=1000, category_id=2)
        ])
        Image.objects.bulk_create([
            Image(space_id=1, url='1.jpg'),
            Image(space_id=2, url='2.jpg')
        ])
        
    def tearDown(self):
        Category.objects.all().delete()
        User.objects.all().delete()
        Host.objects.all().delete()
        Space.objects.all().delete()
        Image.objects.all().delete()
        
    def test_success_space_list_view_get(self):
        client = Client()
        response = client.get('/spaces/lists')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {
            "result": [
                {
                    "title": "space title 1",
                    "sub_title": "space sub title 1",
                    "room_name": "room 1",
                    "price": "1000.00",
                    "detail": "detail 1",
                    "max_capacity": 10,
                    "address": "address 1",
                    "image": ['1.jpg'],
                    "category": 1
                },
                {
                    "title": "space title 2",
                    "sub_title": "space sub title 2",
                    "room_name": "room 2",
                    "price": "1000.00",
                    "detail": "detail 2",
                    "max_capacity": 10,
                    "address": "address 2",
                    "image": ['2.jpg'],
                    "category": 2
                }
            ]
        })