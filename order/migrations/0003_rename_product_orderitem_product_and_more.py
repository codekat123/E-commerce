# Generated by Django 5.2.4 on 2025-07-19 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_order_order_id_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='Product',
            new_name='product',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='adKVcvsB', max_length=8, unique=True),
        ),
    ]
