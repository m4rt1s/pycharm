"""Přihlášení, odhlášení a načtení aktuálního uživatele."""

import secrets

from flask import abort, flash, g, redirect, render_template, request, session, url_for
from . import auth_bp
from data_uzivatel import uzivatele
from.auth_service import AuthService

auth = AuthService(uzivatele)
from werkzeug.security import check_password_hash, generate_password_hash

from . import auth_bp
from data_uzivatel import uzivatele


# Ověření hesla provedeme i pro neexistující účet s náhradním otiskem.
_DUMMY_HASH = generate_password_hash(secrets.token_hex(32))


@auth_bp.before_app_request
def load_user():
    # session pamatuje ID mezi požadavky. g platí jen pro aktuální požadavek.
    user_id = session.get('user_id')
    g.user = None

    for user in uzivatele:
        if user.id == user_id and user.je_aktivni():
            g.user = user
            break

    # Smazaný nebo deaktivovaný účet již nesmí zůstat přihlášený.
    if g.user is None:
        session.pop('user_id', None)


def csrf_token():
    """Vrátí kontrolní kód, který propojuje formulář s touto session."""
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']


@auth_bp.app_context_processor
def auth_context():
    # Tyto hodnoty bude možné používat ve všech HTML šablonách.
    return {'current_user': g.user, 'csrf_token': csrf_token}


def validate_csrf():
    # Chybějící nebo nesprávný kód znamená odmítnutí formuláře (HTTP 400).
    expected = session.get('csrf_token')
    supplied = request.form.get('csrf_token', '')
    if not expected or not secrets.compare_digest(expected, supplied):
        abort(400, description='Platnost formuláře vypršela. Obnov stránku a zkus to znovu.')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Přihlášeného návštěvníka pošleme rovnou na domovskou stránku.
    if g.user:
        return redirect(url_for('index'))
    identity = ''
    error = None
    # GET stránku zobrazí. POST zpracuje vyplněný formulář.
    if request.method == 'POST':
        validate_csrf()
        identity = request.form.get('identity', '').strip()
        password = request.form.get('password', '')
        # casefold sjednotí velikost písmen, takže RADEG i radeg jsou stejné.


        normalized_identity = identity.casefold()
        user = None
        for candidate in uzivatele:
            same_email = normalized_identity == candidate.email.casefold()
            same_nickname = normalized_identity == candidate.nickname.casefold()
            if same_email or same_nickname:
                user = candidate
                break

        password_hash = _DUMMY_HASH
        if user is not None:
            password_hash = user.password
        valid_password = check_password_hash(password_hash, password)
        if not identity:
            error = 'Vyplň e-mail nebo přezdívku.'
        elif user is None:
            # Společné pole rozlišíme podle znaku typického pro e-mail.
            if '@' in identity:
                error = 'Nesprávný e-mail.'
            else:
                error = 'Nesprávná přezdívka.'
        elif not valid_password:
            error = 'Nesprávné heslo.'
        elif not user.je_aktivni():
            error = 'Účet není aktivní.'
        else:
            # Zrušíme původní session i CSRF kód a uložíme pouze ID účtu.
            session.clear()
            session['user_id'] = user.id
            flash(f'Vítej zpět, {user.nickname}!', 'success')
            return redirect(url_for('index'))
    # 200 znamená úspěšné zobrazení, 401 neúspěšné přihlášení.
    status_code = 200
    if error:
        status_code = 401
    return render_template('auth/login.html', identity=identity, error=error), status_code


@auth_bp.post('/logout')
def logout():
    # Odhlášení mění session, proto vyžaduje POST a kontrolu CSRF kódu.
    validate_csrf()
    session.clear()
    flash('Odhlášení proběhlo úspěšně.', 'success')
    return redirect(url_for('index'))

@auth_bp.route('/auth/profile')
def profile():
    if session.get('user_id') is None:
        return redirect(url_for('login'))
    return(redirect(url_for('auth/profile.html')))