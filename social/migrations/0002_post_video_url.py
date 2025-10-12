# Generated manually for adding video_url field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='video_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
