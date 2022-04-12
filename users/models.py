from django.db import models

from utilities.timestamp import TimeStamp

class User(TimeStamp): 
    nickname      = models.CharField(max_length=45)
    email         = models.CharField(max_length=50, unique=True)
    kakao_id      = models.IntegerField()
    date_of_birth = models.DateField()

    class Meta: 
        db_table = 'users'

class Host(TimeStamp): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosts')

    class Meta: 
        db_table = 'hosts'


class WishList(TimeStamp): 
    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    space = models.ForeignKey('spaces.Space', on_delete=models.CASCADE, related_name='wishlists')

    class Meta: 
        db_table = 'wishlists'

class Booking(TimeStamp): 
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking')
    space_size = models.ForeignKey('spaces.Space', on_delete=models.CASCADE, related_name='booking')
    start_time = models.DateTimeField() 
    finish_time  = models.DateTimeField()

    class Meta: 
        db_table = 'booking'

class Status(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='status')
    status  = models.CharField(max_length=50)

    class Meta:
        db_table = 'status'