# Flask obsluhuje webové požadavky; render_template doplní data do HTML šablony.
import os
from pathlib import Path
import secrets

from flask import Flask, render_template
from auth import auth_bp

# __name__ pomůže Flasku najít složky templates a static vedle tohoto souboru.
app = Flask(__name__)
# Klíč podepisuje session s údaji o přihlášení.
# Uložíme jej do instance, aby přihlášení přežilo restart.
secret_path = Path(app.instance_path) / 'secret_key'
secret_path.parent.mkdir(parents=True, exist_ok=True)
if not os.environ.get('SECRET_KEY') and not secret_path.exists():
    try:
        with secret_path.open('x', encoding='utf-8') as secret_file:
            secret_file.write(secrets.token_hex(32))
    except FileExistsError:
        # Jiný proces mohl soubor mezitím vytvořit.
        pass
# SECRET_KEY z prostředí má přednost před místním souborem.
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY') or secret_path.read_text(encoding='utf-8'),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)
# Připojíme přihlašovací část aplikace.
app.register_blueprint(auth_bp)
app.secret_key="kuku"

# Seznam Pokémonů: [] znamená seznam, {} znamená slovník.
# Slovník pojmenovává údaje, takže nemusíme pamatovat jejich pořadí.
# id = číslo Pokédexu, kind = barva v CSS, types = text pro hledání.
# Nového Pokémona přidáš zkopírováním jednoho slovníku.
POKEMON = [
    {
        'id': 25,
        'name': 'Pikachu',
        'kind': 'electric',
        'types': 'Electric',
        'description': 'Elektrický parťák z regionu Kanto.',
    },
    {
        'id': 6,
        'name': 'Charizard',
        'kind': 'fire',
        'types': 'Fire · Flying',
        'description': 'Ohnivý drak s neuvěřitelnou silou.',
    },
    {
        'id': 1,
        'name': 'Bulbasaur',
        'kind': 'grass',
        'types': 'Grass · Poison',
        'description': 'Malý Pokémon se semínkem na zádech.',
    },
    {
        'id': 7,
        'name': 'Squirtle',
        'kind': 'water',
        'types': 'Water',
        'description': 'Vodní Pokémon s pevným krunýřem.',
    },
    {
        'id': 94,
        'name': 'Gengar',
        'kind': 'ghost',
        'types': 'Ghost · Poison',
        'description': 'Tajemný Pokémon ukrytý ve stínech.',
    },
    {
        'id': 133,
        'name': 'Eevee',
        'kind': 'normal',
        'types': 'Normal',
        'description': 'Pokémon s mnoha evolučními možnostmi.',
    },
    {
        'id': 448,
        'name': 'Lucario',
        'kind': 'fighting',
        'types': 'Fighting · Steel',
        'description': 'Mistr aury a bojového umění.',
    },
    {
        'id': 149,
        'name': 'Dragonite',
        'kind': 'dragon',
        'types': 'Dragon · Flying',
        'description': 'Laskavý, ale nesmírně silný drak.',
    },
]


# Dekorátor @app.route propojí adresu / s funkcí index.
# Funkce se zavolá pokaždé, když někdo otevře domovskou stránku.
@app.route('/')
def index():
    pokemon = []

    # Pro každou kartu doplníme adresu obrázku podle čísla Pokédexu.
    for original_pokemon in POKEMON:
        # Kopie zabrání změně původních ukázkových dat.
        card = original_pokemon.copy()
        pokemon_id = card['id']
        card['image'] = (
            'https://raw.githubusercontent.com/PokeAPI/sprites/master/'
            f'sprites/pokemon/other/official-artwork/{pokemon_id}.png'
        )
        pokemon.append(card)

    # V HTML bude seznam dostupný pod názvem pokemon.
    return render_template('index.html', pokemon=pokemon)


# Server se spustí jen při přímém spuštění: python app.py.
# debug=True usnadňuje místní vývoj; pro veřejný provoz jej vypni.
if __name__ == '__main__':
    app.run(debug=True)
