# Generated by Django 3.1.5 on 2021-03-02 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='practice',
            name='teacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='teacher.teacher'),
        ),
    ]
