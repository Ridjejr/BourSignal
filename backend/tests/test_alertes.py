"""Tests du cycle de vie des alertes + autorisation par code de gestion."""

import pytest

from app import db
from app.models.actif import Actif


@pytest.fixture
def actif(app):
    """Insère un actif AAPL (la clé étrangère des alertes pointe dessus)."""
    with app.app_context():
        db.session.add(Actif(ticker="AAPL", nom="Apple Inc.", type="action"))
        db.session.commit()


def creer_alerte(client):
    """Crée une alerte de test et renvoie (id, code_gestion)."""
    response = client.post(
        "/api/alertes",
        json={
            "ticker": "AAPL",
            "condition": "Supérieur à",
            "prix_cible": 200,
            "email": "test@example.com",
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    return data["alerte"]["id"], data["code_gestion"]


def test_creation_renvoie_un_code_et_status_active(client, actif):
    response = client.post(
        "/api/alertes",
        json={
            "ticker": "AAPL",
            "condition": "Supérieur à",
            "prix_cible": 200,
            "email": "test@example.com",
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["code_gestion"]  # code en clair présent une fois
    assert data["alerte"]["status"] == "ACTIVE"
    # Le code/hash ne doit jamais fuiter dans la représentation de l'alerte.
    assert "code_hash" not in data["alerte"]
    assert "code_gestion" not in data["alerte"]


def test_suspendre_puis_reactiver_avec_bon_code(client, actif):
    alerte_id, code = creer_alerte(client)

    r1 = client.patch(f"/api/alertes/{alerte_id}", json={"action": "suspendre", "code": code})
    assert r1.status_code == 200
    assert r1.get_json()["alerte"]["status"] == "SUSPENDED"

    r2 = client.patch(f"/api/alertes/{alerte_id}", json={"action": "reactiver", "code": code})
    assert r2.status_code == 200
    assert r2.get_json()["alerte"]["status"] == "ACTIVE"


def test_mauvais_code_refuse(client, actif):
    alerte_id, _ = creer_alerte(client)

    r = client.patch(f"/api/alertes/{alerte_id}", json={"action": "suspendre", "code": "FAUX"})
    assert r.status_code == 400
    assert "error" in r.get_json()


def test_annuler_est_terminal(client, actif):
    alerte_id, code = creer_alerte(client)

    r1 = client.patch(f"/api/alertes/{alerte_id}", json={"action": "annuler", "code": code})
    assert r1.status_code == 200
    assert r1.get_json()["alerte"]["status"] == "CANCELLED"

    # Plus aucune transition possible depuis CANCELLED.
    r2 = client.patch(f"/api/alertes/{alerte_id}", json={"action": "reactiver", "code": code})
    assert r2.status_code == 400


def test_reactiver_une_alerte_active_est_refuse(client, actif):
    alerte_id, code = creer_alerte(client)

    r = client.patch(f"/api/alertes/{alerte_id}", json={"action": "reactiver", "code": code})
    assert r.status_code == 400


def test_acces_avec_bon_code_renvoie_lalerte(client, actif):
    alerte_id, code = creer_alerte(client)

    r = client.post(f"/api/alertes/{alerte_id}/acces", json={"code": code})
    assert r.status_code == 200
    data = r.get_json()
    assert data["alerte"]["id"] == alerte_id
    assert data["alerte"]["status"] == "ACTIVE"
    assert "code_hash" not in data["alerte"]


def test_acces_avec_mauvais_code_refuse(client, actif):
    alerte_id, _ = creer_alerte(client)

    r = client.post(f"/api/alertes/{alerte_id}/acces", json={"code": "FAUX"})
    assert r.status_code == 403


def test_acces_depuis_une_autre_session_fonctionne(client, actif):
    """Le code donne accès même sans la session d'origine (cas PC partagé)."""
    alerte_id, code = creer_alerte(client)

    # On vide les cookies -> simule un autre navigateur / chez soi.
    client.delete_cookie("session")

    r = client.post(f"/api/alertes/{alerte_id}/acces", json={"code": code})
    assert r.status_code == 200
    assert r.get_json()["alerte"]["id"] == alerte_id