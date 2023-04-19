# Generated by Django 3.2.15 on 2023-04-19 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webgis', '0006_userentry_definition'),
    ]

    operations = [
        migrations.AddField(
            model_name='userentry',
            name='project',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='webgis.projectdefinition'),
            preserve_default=False,
        ),
    ]
