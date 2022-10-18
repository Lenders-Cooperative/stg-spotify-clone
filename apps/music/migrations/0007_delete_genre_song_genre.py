# Generated by Django 4.1.2 on 2022-10-18 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("music", "0006_remove_playlist_songs_songplaylog"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Genre",
        ),
        migrations.AddField(
            model_name="song",
            name="genre",
            field=models.CharField(
                choices=[
                    ("pop", "Pop"),
                    ("country", "Country"),
                    ("rnb", "Rhythm & Blues"),
                    ("hip_hop", "Hip Hop"),
                    ("gospel", "Gospel"),
                    ("kpop", "K-Pop"),
                    ("rock", "Rock 'N Roll"),
                    ("techno", "Techno/Dance"),
                    ("flamenco", "Flamenco"),
                    ("classical", "Classical"),
                ],
                default="pop",
                max_length=100,
            ),
        ),
    ]
