from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_profile_role"),
        ("bookclub", "0002_book_available_to_borrow_book_contributor_and_more"),
    ]

    operations = []
