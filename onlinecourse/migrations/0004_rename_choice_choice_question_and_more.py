# Generated by Django 4.1.5 on 2023-02-24 21:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('onlinecourse', '0003_choiceselection_alter_question_question_text_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='choice',
            new_name='question',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='question',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='question_text',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='choice_text',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='is_correct',
        ),
        migrations.RemoveField(
            model_name='choiceselection',
            name='question',
        ),
        migrations.RemoveField(
            model_name='enrollment',
            name='date_enrolled',
        ),
        migrations.RemoveField(
            model_name='enrollment',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_grade',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='choices',
        ),
        migrations.AddField(
            model_name='choice',
            name='text',
            field=models.CharField(default='choice', max_length=1000),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='enrolled_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='submission',
            name='submitted_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
