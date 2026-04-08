# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_forumpost_visible_to_alter_forumcomment_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumpost',
            name='views',
            field=models.IntegerField(default=0, verbose_name='浏览量'),
        ),
    ]
