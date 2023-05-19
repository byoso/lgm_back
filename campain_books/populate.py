from .models import Game

GAMES = (
    {'name': 'Miscellaneous', 'description': '', 'image_url': ''},
    {'name': 'Dungeons & Dragons', 'description': '', 'image_url': 'https://cdn.shoplightspeed.com/shops/652017/files/45006619/image.jpg'},
    {'name': 'Le Grand Monde', 'description': '', 'image_url': ''},
    {'name': 'Star Wars d6', 'description': '', 'image_url': 'https://www.legrog.org/visuels/gammes/1141.jpg'},
    {'name': 'Star Wars d20', 'description': '', 'image_url': 'https://upload.wikimedia.org/wikipedia/en/a/aa/StarWarsRPG_Revised.jpg'},
    {'name': 'NOC', 'description': '', 'image_url': 'https://d1vzi28wh99zvq.cloudfront.net/images/15046/NOCDTICO.jpg'},
    {'name': 'Dark Heresy', 'description': '', 'image_url': 'https://upload.wikimedia.org/wikipedia/en/6/6b/WH40kRPGCover.jpg'},
    {'name': 'Warhammer', 'description': '', 'image_url': 'https://upload.wikimedia.org/wikipedia/en/7/7d/Warhammer_fantasy_roleplay_cover.jpg'},
    {'name': 'In Nomine Satanis/Magna Veritas', 'description': '', 'image_url': 'https://i0.wp.com/scriiipt.com/wp-content/uploads/2020/05/ins-mv.jpg?w=960&ssl=1'},
    {'name': 'Call of Cthulhu', 'description': '', 'image_url': 'https://upload.wikimedia.org/wikipedia/en/3/33/Call_of_Cthulhu_RPG_1st_ed_1981.jpg'},
    {'name': 'Vampire', 'description': '', 'image_url': 'https://upload.wikimedia.org/wikipedia/en/7/7a/Vampmasq.jpg'},
    {'name': 'Critical', 'description': '', 'image_url': 'https://cf.geekdo-images.com/F6mnkAfdK_pwuTuIuicDMw__imagepagezoom/img/12daQIQzW47QD2XUBAH-gQ6uqCA=/fit-in/1200x900/filters:no_upscale():strip_icc()/pic6858742.jpg'},
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
