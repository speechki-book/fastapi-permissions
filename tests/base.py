from fastapi import FastAPI, Depends
from starlette.testclient import TestClient
from fastapi_permissions import AbstractPermission, OrPermissionsDependency, PermissionsDependency
from httpx import AsyncClient
import pytest


app = FastAPI()


client = TestClient(app)


RESPONSE = {"msg": "Hello World"}
BASE_URL = "http://test"


class TruePermission(AbstractPermission):
    async def has_permissions(self) -> bool:
        return True


class FalsePermission(AbstractPermission):
    async def has_permissions(self) -> bool:
        return False


@app.get(
    "/or_permission_true",
    dependencies=[Depends(OrPermissionsDependency([TruePermission, FalsePermission]))],
)
async def or_permission_true():
    return RESPONSE


@app.get(
    "/or_permission_false",
    dependencies=[Depends(OrPermissionsDependency([FalsePermission]))],
)
async def or_permission_false():
    return RESPONSE


@app.get(
    "/permission_false",
    dependencies=[Depends(PermissionsDependency([FalsePermission]))],
)
async def permission_false():
    return RESPONSE


@app.get(
    "/permission_true",
    dependencies=[Depends(PermissionsDependency([TruePermission]))],
)
async def permission_true():
    return RESPONSE


@pytest.mark.asyncio
async def test_or_permission_true():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get("/or_permission_true")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_or_permission_false():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get("/or_permission_false")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_permission_true():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get("/permission_true")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_permission_false():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get("/permission_false")
    assert response.status_code == 403
