# Generated by Django 3.1.1 on 2020-10-02 13:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('menu_cards', '0005_auto_20200929_1035'),
    ]

    operations = [
        migrations.CreateModel(
            name='DishPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('image', models.ImageField(upload_to='photo', validators=[django.core.validators.FileExtensionValidator(['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG', 'gif', 'GIF'])])),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='menu_cards.dish')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
