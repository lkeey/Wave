# Generated by Django 4.0.6 on 2022-08-08 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0011_chat_alter_message_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='date_cerated',
            new_name='date_created',
        ),
    ]