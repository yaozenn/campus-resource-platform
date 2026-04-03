from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0004_pointrecord_rename_image_prize_image_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='prize',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='是否上架'),
        ),
    ]
