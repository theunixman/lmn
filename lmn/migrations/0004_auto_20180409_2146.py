# Generated by Django 2.0.3 on 2018-04-10 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmn', '0003_auto_20180409_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='pictures/'),
        ),
    ]