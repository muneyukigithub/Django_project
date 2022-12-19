# Generated by Django 3.2.14 on 2022-11-21 12:49

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Eメールアドレス')),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_id', models.UUIDField(default=uuid.UUID('59dc92cc-f5c5-4e06-a9d7-6a8d81ec1e0e'), editable=False, primary_key=True, serialize=False, verbose_name='タスクID')),
                ('task', models.CharField(max_length=255, verbose_name='タスク')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='作成日')),
            ],
        ),
        migrations.CreateModel(
            name='SmallTask',
            fields=[
                ('smalltask_id', models.UUIDField(default=uuid.UUID('198e6fce-0971-4aff-849c-a6d6cce9bc72'), primary_key=True, serialize=False, verbose_name='小タスクID')),
                ('smalltask', models.CharField(max_length=255, verbose_name='小タスク')),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drf_test_app.task')),
            ],
        ),
    ]
