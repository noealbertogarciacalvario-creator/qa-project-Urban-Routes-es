def test_create_post(api_client):
    response = api_client.create_post(
        title="QA Automation",
        body="API testing with requests",
        user_id=1
    )

    data = response.json()

    assert response.status_code == 201
    assert data["title"] == "QA Automation"
    assert data["body"] == "API testing with requests"
    assert data["userId"] == 1


def test_get_post(api_client):
    response = api_client.get_post(1)

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == 1
    assert "title" in data