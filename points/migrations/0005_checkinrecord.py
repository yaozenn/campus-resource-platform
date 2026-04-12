from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0004_pointrecord_rename_image_prize_image_url_and_more'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckInRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkin_date', models.DateField(verbose_name='签到日期')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkin_records', to='users.user', verbose_name='用户')),
            ],
            options={
                'verbose_name': '签到记录',
                'verbose_name_plural': '签到记录',
                'ordering': ['-checkin_date', '-created_at'],
                'unique_together': {('user', 'checkin_date')},
            },
        ),
    ]
