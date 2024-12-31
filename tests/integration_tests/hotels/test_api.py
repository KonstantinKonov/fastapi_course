async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2024-08-01",
            "date_to": "2024-08-10",
        }
    )
    print(f"{response.json()=}")

    assert response.status_code == 200


async def test_get_facilities(ac):
    response = await ac.get(
        "/facilities",
    )

    assert response.status_code == 200


async def test_post_facilities(ac):
    response = await ac.get(
        "/facilities",
        json={
            'id': 1,
            'title': 'facility title'
        }
    )

    assert response.status_code == 200