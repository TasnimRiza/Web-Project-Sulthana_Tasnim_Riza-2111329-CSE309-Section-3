from django.db import migrations
from learning.catalog import LETTER_CATALOG


def seed_letters(apps, schema_editor):
    Letter = apps.get_model("learning", "Letter")
    for item in LETTER_CATALOG:
        Letter.objects.update_or_create(
            language=item["language"],
            symbol=item["symbol"],
            defaults={
                "slug": f"{item['language']}-{item['sort_order']}",
                "name": item["name"],
                "transliteration": item["transliteration"],
                "word": item["word"],
                "word_translation": item["word_translation"],
                "emoji": item["emoji"],
                "description": item["description"],
                "speech_text": item["speech_text"],
                "sort_order": item["sort_order"],
                "is_active": True,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("learning", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_letters, migrations.RunPython.noop),
    ]
