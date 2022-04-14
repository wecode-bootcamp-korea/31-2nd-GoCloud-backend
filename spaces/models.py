from django.db import models

from utilities.timestamp import TimeStamp

class Category(models.Model): 
    title = models.CharField(max_length=100)

    class Meta: 
        db_table = 'categories'

class Space(TimeStamp): 
    host         = models.ForeignKey('users.Host', on_delete=models.CASCADE, related_name='spaces')
    title        = models.CharField(max_length=100)
    sub_title    = models.CharField(max_length=100)
    room_name    = models.CharField(max_length=45)
    detail       = models.TextField()
    max_capacity = models.IntegerField()
    address      = models.CharField(max_length=100)
    price        = models.DecimalField(max_digits=30, decimal_places=2)
    category     = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='spaces')

    class Meta: 
        db_table = 'spaces'

class Image(models.Model): 
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='images')
    url   = models.CharField(max_length=200)

    class Meta: 
        db_table = 'images'

class Review(TimeStamp): 
    user      = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reviews')
    space     = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='reviews')
    content   = models.TextField()
    image_url = models.CharField(max_length=200)

    class Meta: 
        db_table = 'reviews'