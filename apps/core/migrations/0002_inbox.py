# Generated by Django 3.2 on 2021-04-12 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('subject', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='core.member')),
            ],
            options={
                'db_table': 'inbox',
            },
        ),
    ]
