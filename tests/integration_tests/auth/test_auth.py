import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("homer@simpsons.com", "hash", 200),
        ("marge@simpsons.com", "hash", 200),
        ("lisa@simpsons.com", "hash", 200),
        ("bart@simpsons.com", "hash", 200),
        ("meggy@simpsons.com", "hash", 200),
        ("wrong.com", "hash", 422),
        ("wrong@wrong", "hash", 422),
    ],
)
async def test_integr_auth(email: str, password: str, status_code: int, ac):
    # /register
    res = await ac.post("/auth/register", json={"email": email, "password": password})
    assert res.status_code == status_code
    if status_code != 200:
        return
    # /login
    res = await ac.post("/auth/login", json={"email": email, "password": password})
    assert res.status_code == 200
    assert "access_token" in res.json()
    # get /me
    res = await ac.get("/auth/me")
    assert res.status_code == 200
    assert res.json()["email"] == email
    # /logout
    res = await ac.post("/auth/logout")
    assert res.status_code == 200
    assert not ("access_token" in ac.cookies)
