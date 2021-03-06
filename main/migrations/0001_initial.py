# Generated by Django 3.1 on 2021-11-11 05:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BirdingCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birding_category', models.CharField(max_length=100)),
                ('category_summary', models.CharField(max_length=500)),
                ('category_slug', models.SlugField(max_length=100)),
                ('category_image', models.FileField(upload_to=main.models.BirdingCategory.user_directory_path)),
            ],
            options={
                'verbose_name_plural': 'Birding Categories',
            },
        ),
        migrations.CreateModel(
            name='ConservationCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conservation_category', models.CharField(max_length=100)),
                ('category_summary', models.CharField(max_length=500)),
                ('category_slug', models.SlugField(max_length=100)),
                ('category_image', models.FileField(upload_to=main.models.ConservationCategory.user_directory_path)),
            ],
            options={
                'verbose_name_plural': 'Conservation Categories',
            },
        ),
        migrations.CreateModel(
            name='ConservationContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conservation_content', models.CharField(max_length=100)),
                ('content_text', models.TextField()),
                ('content_time', models.DateTimeField(auto_now_add=True)),
                ('content_file', models.FileField(blank=True, null=True, upload_to=main.models.ConservationContent.user_directory_path)),
                ('content_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.conservationcategory', verbose_name='Category')),
                ('content_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name_plural': 'Conservation Content',
            },
        ),
        migrations.CreateModel(
            name='BirdingContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birding_content', models.CharField(max_length=100)),
                ('content_text', models.TextField()),
                ('content_time', models.DateTimeField(auto_now_add=True)),
                ('content_file', models.FileField(blank=True, null=True, upload_to=main.models.BirdingContent.user_directory_path)),
                ('content_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.birdingcategory', verbose_name='Category')),
                ('content_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name_plural': 'Birding Content',
            },
        ),
    ]
