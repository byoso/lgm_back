from .models import Game

GAMES = (
    {
        'name': 'Miscellaneous', 'description': '', 'image_url': '',
        'official_site': '',
        'official_site': ''
    },
    {
        'name': 'Dungeons & Dragons', 'description': '',
        'image_url': 'https://cdn.shoplightspeed.com/shops/652017/files/45006619/image.jpg',
        'official_site': 'https://dnd.wizards.com/'
    },
    {
        'name': 'Le Grand Monde', 'description': '',
        'image_url': '',
        'official_site': ''
    },
    {
        'name': 'Star Wars d6', 'description': '',
        'image_url': 'https://www.legrog.org/visuels/gammes/1141.jpg',
        'official_site': 'http://d6holocron.com/downloads/wegcore.html'
    },
    {
        'name': 'Star Wars', 'description': '',
        'image_url': 'https://images-cdn.fantasyflightgames.com/filer_public/e0/ad/e0ad89ab-f108-42cb-b8d4-4013a466b673/swa01_slider_mobile.jpg',
        'official_site': 'https://www.fantasyflightgames.com/en/star-wars-age-rebellion-showcase/'
    },
    {
        'name': 'NOC', 'description': '',
        'image_url': 'https://d1vzi28wh99zvq.cloudfront.net/images/15046/NOCDTICO.jpg',
        'official_site': 'https://sethmes-editions.com/noc/'
    },
    {
        'name': 'Dark Heresy', 'description': '',
        'image_url': 'http://wh40krpgtools.s3.amazonaws.com/images/books/Dark_Heresy_Core-1.jpg',
        'official_site': 'https://www.40krpgtools.com/library/dark-heresy/dark-heresy-core-rulebook/'
    },
    {
        'name': 'Warhammer', 'description': '',
        'image_url': 'https://upload.wikimedia.org/wikipedia/en/7/7d/Warhammer_fantasy_roleplay_cover.jpg',
        'official_site': 'https://cubicle7games.com/our-games/warhammer-fantasy-roleplay'
    },
    {
        'name': 'In Nomine Satanis/Magna Veritas',
        'description': '', 'image_url': 'https://i0.wp.com/scriiipt.com/wp-content/uploads/2020/05/ins-mv.jpg?w=960&ssl=1',
        'official_site': 'https://raise-dead.com/shop/'
    },
    {
        'name': 'Call of Cthulhu', 'description': '',
        'image_url': 'https://upload.wikimedia.org/wikipedia/en/3/33/Call_of_Cthulhu_RPG_1st_ed_1981.jpg',
        'official_site': 'https://www.chaosium.com/call-of-cthulhu-rpg/'
    },
    {
        'name': 'Vampire', 'description': '',
        'image_url': 'https://upload.wikimedia.org/wikipedia/en/7/7a/Vampmasq.jpg',
        'official_site': 'https://www.worldofdarkness.com/vampire-the-masquerade'
    },
    {
        'name': 'Critical', 'description': '',
        'image_url': 'https://cf.geekdo-images.com/F6mnkAfdK_pwuTuIuicDMw__imagepagezoom/img/12daQIQzW47QD2XUBAH-gQ6uqCA=/fit-in/1200x900/filters:no_upscale():strip_icc()/pic6858742.jpg',
        'official_site': 'https://www.hachetteboardgames.com/products/critical-foundation-season-1'
    },
)


def populate_games():
    """Populate the database with some games"""
    if Game.objects.count() == 0:
        for game in GAMES:
            Game.objects.get_or_create(
                name=game['name'],
                description=game['description'],
                image_url=game['image_url'],
                official_site=game['official_site'])
        print("Populated the database with some games")


def populate():
    populate_games()
