def test_health_endpoint_returns_up(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "UP"
    assert payload["service"] == "boursignal-api"


def test_unknown_route_returns_404(client):
    response = client.get("/api/this-route-does-not-exist")
    assert response.status_code == 404
