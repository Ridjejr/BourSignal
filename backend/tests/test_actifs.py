from unittest.mock import patch


def test_search_without_query_returns_400(client):
    response = client.get("/api/actifs/search")
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_search_with_blank_query_returns_400(client):
    response = client.get("/api/actifs/search?q=   ")
    assert response.status_code == 400


def test_search_with_unknown_ticker_returns_404(client):
    with patch("app.services.actif_service.ActifService.rechercher", return_value=None):
        response = client.get("/api/actifs/search?q=ZZZZ")
    assert response.status_code == 404


def test_search_returns_data_when_found(client):
    fake_payload = {"ticker": "AAPL", "nom": "Apple Inc."}
    with patch(
        "app.services.actif_service.ActifService.rechercher",
        return_value=fake_payload,
    ):
        response = client.get("/api/actifs/search?q=AAPL")

    assert response.status_code == 200
    assert response.get_json() == fake_payload
