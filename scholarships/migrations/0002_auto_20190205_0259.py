# Generated by Django 2.1.3 on 2019-02-05 02:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DataEntryQuestion',
        ),
        migrations.DeleteModel(
            name='FileSubmitQuestion',
        ),
        migrations.RemoveField(
            model_name='multiplechoicequestionoption',
            name='multiple_choice_question',
        ),
        migrations.RemoveField(
            model_name='question',
            name='application',
        ),
        migrations.DeleteModel(
            name='ShortAnswerQuestion',
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='application',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='applications.Application'),
        ),
        migrations.DeleteModel(
            name='Application',
        ),
        migrations.DeleteModel(
            name='MultipleChoiceQuestion',
        ),
        migrations.DeleteModel(
            name='MultipleChoiceQuestionOption',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]