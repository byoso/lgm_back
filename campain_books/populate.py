from .models import Game

GAMES = (
    {'name': 'Miscellaneous', 'description': 'Miscellaneous', 'image_url': ''},
    {'name': 'Dungeons & Dragons', 'description': 'Miscellaneous', 'image_url': ''},
    {'name': 'Le Grand Monde', 'description': 'Miscellaneous', 'image_url': ''},
    {'name': 'Star Wars d6', 'description': 'Miscellaneous', 'image_url': ''},
    {'name': 'Star Wars d20', 'description': 'Miscellaneous', 'image_url': ''},
    {'name': 'NOC', 'description': 'Miscellaneous', 'image_url': ''},
    {'name': 'Dark Heresy', 'description': 'Miscellaneous', 'image_url': ''},
    {'name': 'Warhammer', 'description': 'Miscellaneous', 'image_url': ''},
    {'name': 'In Nomine Satanis/Magna Veritas', 'description': 'Miscellaneous', 'image_url': ''},
    {'name': 'Call of Cthulhu', 'description': 'Miscellaneous', 'image_url': ''},
    {'name': 'Vampire', 'description': 'Miscellaneous', 'image_url': ''},
    {'name': 'Critical', 'description': 'Miscellaneous', 'image_url': ''},
)


def populate_games():
    """Populate the database with some games"""
    if Game.objects.count() == 0:
        for game in GAMES:
            Game.objects.get_or_create(
                name=game['name'],
                description=game['description'],
                image_url=game['image_url'])
        print("Populated the database with some games")


def populate():
    populate_games()
