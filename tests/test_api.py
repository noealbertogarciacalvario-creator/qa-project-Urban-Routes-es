from api.client import APIClient


def test_create_post():
    client = APIClient()

    response = client.create_post(
        title="QA Automation",
        body="API testing with requests",
        user_id=1
    )

    assert response.status_code == 201
    assert response.json()["title"] == "QA Automation"
    assert response.json()["body"] == "API testing with requests"
    assert response.json()["userId"] == 1


def test_get_post():
    client = APIClient()

    response = client.get_post(1)

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert "title" in response.json()