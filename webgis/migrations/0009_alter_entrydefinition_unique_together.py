# Generated by Django 3.2.15 on 2023-04-19 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webgis', '0008_alter_userentry_project'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='entrydefinition',
            unique_together={('name', 'field_definition')},
        ),
    ]
