# Generated by Django 4.0.4 on 2022-07-31 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_admin', '0003_for_transfer'),
    ]

    operations = [
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(through='movies_admin.PersonFilmwork', to='movies_admin.person', verbose_name='person'),
        ),
        migrations.AlterField(
            model_name='personfilmwork',
            name='role',
            field=models.CharField(choices=[('ACTOR', 'actor'), ('DIRECTOR', 'director'), ('WRITER', 'writer')], max_length=16, null=True),
        ),
    ]
