# PokéApp — průvodce pro začátečníka

PokéApp je malý web napsaný v Pythonu pomocí Flasku. Zobrazuje osm ukázkových Pokémonů, umí v nich vyhledávat, filtrovat je podle typu a přihlásit trenéra.

## Kde začít

Čti soubory v tomto pořadí:

1. `app.py` — vytvoření aplikace, data Pokémonů a domovská stránka.
2. `templates/base.html` — společná kostra všech stránek.
3. `templates/index.html` a `templates/components/main.html` — obsah Pokédexu a opakování karet.
4. `auth/templates/auth/login.html` — přihlašovací formulář.
5. `auth/routes.py` — zpracování přihlášení a odhlášení.
6. `models/user.py` a `data_uzivatel.py` — uživatel a ukázkové účty.
7. `static/effects.js` — vyhledávání, filtry a animace v prohlížeči.
8. `static/css/style.css` — barvy, velikosti, rozložení a animace vzhledu.

## Jak otevření stránky funguje

Když otevřeš `/`, Flask v `app.py` zavolá funkci `index()`. Ta připraví seznam Pokémonů a předá jej do `index.html`. Šablona převezme kostru `base.html` a vloží do ní `components/main.html`. Cyklus v této komponentě vytvoří jednu kartu pro každého Pokémona. Výsledné HTML se odešle prohlížeči. Ten načte CSS a JavaScript.

Python běží na serveru. JavaScript běží v prohlížeči: filtrování karet nepotřebuje nový požadavek na server. Při změně dat v Pythonu je potřeba stránku znovu načíst.

## Mapa projektu

| Soubor nebo složka | Úloha |
| --- | --- |
| `app.py` | Spuštění Flasku, nastavení a cesta `/` |
| `auth/__init__.py` | Skupina přihlašovacích stránek, tzv. Blueprint |
| `auth/routes.py` | Cesty `/auth/login` a `/auth/logout`, session a CSRF |
| `models/user.py` | Třída `User` a její metody |
| `data_uzivatel.py` | Ukázkové účty v paměti, bez databáze |
| `templates/components/menu.html` | Navigace a odhlašovací formulář |
| `templates/components/header.html` | Úvodní banner |
| `templates/components/main.html` | Hledání, karty a informační sekce |
| `templates/components/footer.html` | Patička |
| `templates/admin.html`, `templates/abouth.html` | Prázdné rezervní šablony, zatím bez Flask cest |
| `static/` | CSS a JavaScript posílané přímo prohlížeči |
| `tests/test_auth.py` | Automatická kontrola přihlášení a stránek |
| `instance/secret_key` | Automaticky vytvořený podpisový klíč session |

## Základní zápisy

- Python: `[]` je seznam, `{ 'name': 'Pikachu' }` je slovník. `for` prochází položky, `if` ověřuje podmínku, `def` vytváří funkci a `return` vrací výsledek.
- Jinja: `{{ hodnota }}` vypíše hodnotu z Pythonu. `{% if ... %}` rozhoduje, co zobrazit. `{% for ... %}` opakuje HTML. `{# ... #}` je komentář, který se návštěvníkovi neposílá.
- HTML: `class` propojuje prvek se styly, `id` jej pojmenuje pro odkaz nebo JavaScript. `name` u vstupu určuje název odeslaného údaje.
- CSS: `.auth-card` vybírá třídu, `padding` přidává vnitřní mezeru a `margin` vnější. `@media` upravuje vzhled podle velikosti obrazovky nebo nastavení pohybu.
- JavaScript: `const` pojmenuje hodnotu, `let` hodnotu, která se může měnit. `addEventListener` určuje, co se stane po kliknutí nebo při psaní. `dataset` čte HTML atributy `data-*`.

## Jak funguje přihlášení

1. GET `/auth/login` zobrazí formulář a vytvoří CSRF kód v session.
2. Tlačítko odešle pomocí POST pole `identity`, `password` a `csrf_token`.
3. Flask zkontroluje kód, najde účet podle e-mailu nebo přezdívky a ověří otisk hesla.
4. Při úspěchu uloží do session ID uživatele a přesměruje na `/`.
5. Před každým dalším požadavkem `load_user()` vyhledá tento účet a uloží jej do `g.user`. Šablony jej dostanou jako `current_user`.
6. Odhlášení zkontroluje CSRF kód a smaže session.

Session používá podepsanou cookie. Nepatří do ní hesla. CSRF kód pomáhá odmítnout podvržené odeslání formuláře. Tyto části ponech i při dalších úpravách.

## Spuštění a kontrola

V PyCharmu spusť soubor `app.py` pomocí projektového interpretu. Adresa se vypíše do konzole, obvykle `http://127.0.0.1:5000`.

V PowerShellu v kořenové složce tohoto projektu můžeš použít:

```powershell
.\.venv\Scripts\python.exe app.py
```

Ukázkový účet pro místní vyzkoušení: přezdívka `radeg`, heslo `123`. Další účty najdeš v `data_uzivatel.py`. Účty jsou výukové, pro veřejné použití by potřebovaly skutečné ukládání a silná hesla. `debug=True` v `app.py` slouží pro místní vývoj.

Existující testy spustíš:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Obrázky, Bootstrap, ikony a fonty se načítají z internetu.

## První vlastní úpravy

- Změna Pokémona: uprav slovník v seznamu `POKEMON` v `app.py`. Pro nový záznam použij skutečné číslo Pokédexu, aby odpovídal obrázek.
- Změna textu přihlášení: uprav `auth/templates/auth/login.html`. Názvy polí `identity`, `password` a `csrf_token` odpovídají kódu v `auth/routes.py`.
- Změna barvy tlačítek: najdi `--yellow` ve `static/css/style.css`.
- Změna chování filtrů: najdi funkci `updateCards` v `static/effects.js`.

Začni jednou drobnou změnou, ulož soubor a obnov stránku. Snáz tak poznáš, která část kódu co ovlivňuje.
