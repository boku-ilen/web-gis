# Generated by Django 3.2.15 on 2023-04-19 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webgis', '0005_alter_userentry_geom'),
    ]

    operations = [
        migrations.AddField(
            model_name='userentry',
            name='definition',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='webgis.entrydefinition'),
            preserve_default=False,
        ),
    ]
