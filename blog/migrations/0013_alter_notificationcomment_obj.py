# Generated by Django 4.0.6 on 2022-08-07 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_alter_notificationcomment_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationcomment',
            name='obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_notifications_like', to='blog.comment'),
        ),
    ]
