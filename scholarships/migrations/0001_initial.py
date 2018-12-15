# Generated by Django 2.1.3 on 2018-12-08 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicField',
            fields=[
                ('field_name', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='DataEntryQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='FileSubmitQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='KeyWord',
            fields=[
                ('key_word', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='MultipleChoiceQuestionOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=40)),
                ('multiple_choice_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scholarships.MultipleChoiceQuestion')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(choices=[('MC', 'Multiple Choice'), ('SA', 'Short Answer'), ('FS', 'File Submit'), ('DA', 'Data Entry')], max_length=2)),
                ('order', models.CharField(max_length=20)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scholarships.Application')),
            ],
        ),
        migrations.CreateModel(
            name='Scholarship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('required_gpa', models.FloatField()),
                ('description', models.CharField(max_length=2000)),
                ('visible', models.BooleanField(default=False)),
                ('application', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scholarships.Application')),
                ('fields', models.ManyToManyField(related_name='fields', to='scholarships.AcademicField')),
                ('key_words', models.ManyToManyField(related_name='scholarships', to='scholarships.KeyWord')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.DonorProfile')),
            ],
        ),
        migrations.CreateModel(
            name='ShortAnswerQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=300)),
            ],
        ),
    ]