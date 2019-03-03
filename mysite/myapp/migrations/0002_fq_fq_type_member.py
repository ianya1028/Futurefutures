# Generated by Django 2.1.4 on 2019-02-22 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fq_id', models.CharField(max_length=2)),
                ('fq_question', models.TextField()),
                ('fq_choice1', models.CharField(default='', max_length=50)),
                ('fq_choice2', models.CharField(default='', max_length=50)),
                ('fq_choice3', models.CharField(default='', max_length=50)),
                ('fq_choice4', models.CharField(default='', max_length=50, null=True)),
                ('fq_choice5', models.CharField(default='', max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FQ_type',
            fields=[
                ('type_id', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('type_name', models.CharField(max_length=20)),
                ('type_score', models.CharField(default='', max_length=20)),
                ('type_describe', models.TextField(default='', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('member_id', models.AutoField(primary_key=True, serialize=False)),
                ('member_name', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=50)),
                ('phone_num', models.CharField(max_length=12)),
                ('type', models.CharField(max_length=3, null=True)),
            ],
        ),
    ]