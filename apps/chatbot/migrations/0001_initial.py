# Generated by Django 4.0.1 on 2022-04-06 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('flag', models.CharField(max_length=50)),
                ('verify', models.IntegerField(default=0)),
                ('url', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Menu',
                'db_table': 'cb_menus',
            },
        ),
        migrations.CreateModel(
            name='SubMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('sequence', models.IntegerField()),
                ('menu_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot.menu')),
            ],
            options={
                'verbose_name_plural': 'Sub Menus',
                'db_table': 'cb_sub_menus',
            },
        ),
        migrations.CreateModel(
            name='MenuLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='link', to='chatbot.menu')),
                ('menu_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu', to='chatbot.menu')),
                ('sub_menu_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chatbot.submenu')),
            ],
            options={
                'verbose_name_plural': 'Menu Links',
                'db_table': 'cb_menu_links',
            },
        ),
    ]