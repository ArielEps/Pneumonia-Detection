def test_home(client):
    response = client.get("/")
    assert b"<title>Document</title>" in response.data