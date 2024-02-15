import os
from typing import Annotated, Sequence

from fastapi import (
    APIRouter, 
    Depends,
    UploadFile,
    HTTPException,
    status
)
from fastapi.responses import StreamingResponse

import magic

from bluestorage.setting import setting
from bluestorage.util import get_hash

from bluestorage.databases.query import Query
from bluestorage.databases.schema import ItemInfo, User

from bluestorage.api import app
from bluestorage.api.auth import get_current_user

api_router = APIRouter()

@api_router.get("/")
async def root() -> dict:
    return {"status": "running"}


@api_router.get("/items")
async def read_items(
    query: Annotated[Query, Depends(app.get_query)],
    user: Annotated[User, Depends(get_current_user)]
) -> Sequence[ItemInfo]:
    _ = user
    data = await query.iteminfo.read_all() 
    return data

@api_router.post("/items", status_code=status.HTTP_201_CREATED)
async def upload_item(
    query: Annotated[Query, Depends(app.get_query)],
    _: Annotated[User, Depends(get_current_user)],
    item: UploadFile, 
) -> dict:

    key = get_hash(item)
    content = await item.read()
    assert item.filename

    path = os.path.join(setting["DB"]["upload_dir"], item.filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fp:
        fp.write(content)

    await query.iteminfo.create(
        ItemInfo(
            id=key,
            name=item.filename,
            path=path,
        )
    )

    return {"id": key}


@api_router.get("/items/{id}")
async def read_item(
    query: Annotated[Query, Depends(app.get_query)],
    _: Annotated[User, Depends(get_current_user)],
    id: str, 
) -> StreamingResponse:
 
    item = await query.iteminfo.read(id)
    if not item:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    
    def iter():
        with open(item.path, "rb") as file_like:
            while chuck := file_like.read(1024):
                yield chuck

    return StreamingResponse(
        iter(),
        media_type=magic.from_file(item.path, mime=True),
    )

@api_router.put("/items/{id}")
async def update_item(
    query: Annotated[Query, Depends(app.get_query)],
    _: Annotated[User, Depends(get_current_user)],
    id: str, 
    name: str,
):
    item = await query.iteminfo.read(id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    item.name = name
    # path real item update
    await query.iteminfo.update(item)

@api_router.delete("/items/{id}")
async def delete_item(
    query: Annotated[Query, Depends(app.get_query)],
    _: Annotated[User, Depends(get_current_user)],
    id: str,
):
    item = await query.iteminfo.read(id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    os.remove(item.path)
    await query.iteminfo.delete(item)
    return

