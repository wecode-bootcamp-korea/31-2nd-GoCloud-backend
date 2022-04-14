# Generated by Django 4.0.3 on 2022-04-15 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spacesize',
            name='size',
        ),
        migrations.RemoveField(
            model_name='spacesize',
            name='space',
        ),
        migrations.AddField(
            model_name='review',
            name='image_url',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='space',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='space',
            name='room_name',
            field=models.CharField(default=1, max_length=45),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='space',
            name='sub_title',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Size',
        ),
        migrations.DeleteModel(
            name='SpaceSize',
        ),
    ]
