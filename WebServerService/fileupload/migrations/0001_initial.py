# Generated by Django 4.1.5 on 2023-01-16 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, null=True)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
