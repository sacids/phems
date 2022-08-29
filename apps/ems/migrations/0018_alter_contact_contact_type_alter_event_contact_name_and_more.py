# Generated by Django 4.0.1 on 2022-06-20 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0017_alter_contact_contact_type_alter_event_contact_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='contact_type',
            field=models.CharField(choices=[('ADDRESS', 'Address'), ('EMAIL', 'E-mail'), ('PHONE', 'Phone Number')], default='PHONE', max_length=15),
        ),
        migrations.AlterField(
            model_name='event',
            name='contact_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='contact_phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
