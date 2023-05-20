def test_home(client):
    response = client.get("/")
    assert b"gg" in response.data