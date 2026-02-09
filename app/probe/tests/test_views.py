from httpx import AsyncClient, codes

from app.main import app


async def test_live_probe(client: AsyncClient) -> None:
    response = await client.get(app.url_path_for("live_probe"))

    assert response.status_code == codes.OK
    assert response.text == '"ok"'


async def test_health_probe(client: AsyncClient) -> None:
    response = await client.get(app.url_path_for("health_probe"))

    assert response.status_code == codes.OK
    assert response.text == '"app and database ok"'
