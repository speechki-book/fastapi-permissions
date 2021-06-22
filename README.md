# fastapi-permissions

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


Introduction
------------
Utils for FastAPI. Permission dependencies.

## Examples

### OrPermissionsDependency

TruePermission or FalsePermission - return **True**

```python
from fastapi import APIRouter, Depends
from fastapi_permissions import AbstractPermission, OrPermissionsDependency
router = APIRouter()


class TruePermission(AbstractPermission):
    async def has_permissions(self) -> bool:
        return True

    
class FalsePermission(AbstractPermission):
    async def has_permissions(self) -> bool:
        return False
    
@router.get(
    "/api/v1/test/",
    tags=["test.v1"],
    dependencies=[
        Depends(
            OrPermissionsDependency(
                [TruePermission, FalsePermission]
            )
        )
    ],
)
async def test_handler():
    return {"detail": "Hello World!"}
```


### PermissionsDependency

TruePermission and FalsePermission - return **False**


```python
from fastapi import APIRouter, Depends
from fastapi_permissions import AbstractPermission, PermissionsDependency
router = APIRouter()


class TruePermission(AbstractPermission):
    async def has_permissions(self) -> bool:
        return True

    
class FalsePermission(AbstractPermission):
    async def has_permissions(self) -> bool:
        return False
    
@router.get(
    "/api/v1/test/",
    tags=["test.v1"],
    dependencies=[
        Depends(
            PermissionsDependency(
                [TruePermission, FalsePermission]
            )
        )
    ],
)
async def test_handler():
    return {"detail": "Hello World!"}


@router.get(
    "/api/v1/test_1/",
    tags=["test.v1"],
    dependencies=[
        Depends(
            PermissionsDependency(
                [TruePermission]
            )
        )
    ],
)
async def test_handler():
    return {"detail": "Hello World!"}
```


## Installation

------------
   `$ pip install git+https://github.com/speechki-book/fastapi-permissions`
   

Dependencies
------------

1. FastAPI