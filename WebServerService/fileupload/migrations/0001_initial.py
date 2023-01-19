# Generated by Django 4.1.5 on 2023-01-19 02:41

import Commons.common
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
                ('gc_no', models.CharField(max_length=256, null=True)),
                ('fname', models.CharField(max_length=256, null=True)),
                ('toUpFile', models.FileField(blank=True, upload_to=Commons.common.get_upload_file_path)),
                ('toUpFile_url', models.CharField(max_length=256, null=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
