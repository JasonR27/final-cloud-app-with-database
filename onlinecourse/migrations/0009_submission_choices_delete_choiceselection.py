# Generated by Django 4.1.5 on 2023-02-25 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinecourse', '0008_alter_choiceselection_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='choices',
            field=models.ManyToManyField(to='onlinecourse.choice'),
        ),
        migrations.DeleteModel(
            name='ChoiceSelection',
        ),
    ]