# Generated by Django 2.0.7 on 2018-07-30 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PostUrl',
        ),
        migrations.DeleteModel(
            name='SourceUrl',
        ),
        migrations.DeleteModel(
            name='Url',
        ),
        migrations.AddField(
            model_name='post',
            name='originalUrl',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='value',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=120, null=True),
        ),
    ]
