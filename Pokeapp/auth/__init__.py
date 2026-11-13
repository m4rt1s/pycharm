"""Blueprint sdružuje stránky související s přihlášením."""

from flask import Blueprint

# Všechny zdejší adresy začínají /auth, například /auth/login.
auth_bp = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth',
    template_folder='templates',
)

# Routy načítáme až po vytvoření auth_bp, protože jej samy používají.
from . import routes
