# Generated by Django 3.2.12 on 2022-03-23 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bugbase', '0003_sample_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sample_data',
            old_name='sample_id',
            new_name='sample',
        ),
    ]
