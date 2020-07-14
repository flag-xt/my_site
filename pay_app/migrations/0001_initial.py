# Generated by Django 2.2.2 on 2020-07-13 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('net_app', '0004_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('out_trade_num', models.UUIDField()),
                ('order_num', models.CharField(max_length=50)),
                ('trade_no', models.CharField(default='', max_length=120)),
                ('status', models.CharField(default='待支付', max_length=20)),
                ('payway', models.CharField(default='alipay', max_length=20)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='net_app.Address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='net_app.User')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goodsid', models.PositiveIntegerField()),
                ('colorid', models.PositiveIntegerField()),
                ('sizeid', models.PositiveIntegerField()),
                ('count', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pay_app.Order')),
            ],
        ),
    ]