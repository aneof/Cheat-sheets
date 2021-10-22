from enum import Enum
from typing import Optional, List, Dict, Set
from fastapi import FastAPI, Query, Path, Body, Cookie, Header
from pydantic import BaseModel, Field, HttpUrl, EmailStr


# pydantic classes for request body
class BodyItem(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None,
    tags: Set[str] = set()

class BodyUser(BaseModel):
    username: str
    full_name: Optional[str] = None


# base class for enum example
# this is how we define Enums (important)
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


# GET path operation function
@app.get("/")
async def root():
    return {"message": "Hello World"}


# type declaration allows automatic conversion from HTTP request to Python data
# (and editor support)
# (and type validation thanks to pydantic)
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


# fixed path must be listed before variable path to avoid conflict
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the_current_user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# enum example
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    # different way to import residuals
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}


# adding a path parameter is possible but no documentation is available then
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# query parameters: set of key-value pairs (after the ? in URL, separated by &)
fake_items_df = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/db_items")
async def read_db_item(skip: int = 0, limit: int = 10):
    return fake_items_df[skip : skip + limit]


# pydantic request body validation example
# it enables editor support for received item
@app.post("/body_items/")
async def create_item(item: BodyItem):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/body_items/{item_id}")
async def update_item(item_id: int, item: BodyItem):
    return {"item_id": item_id, **item.dict()}


# string validation examples for query parameters
# Query(default value, validation_rule) instead of default value
@app.get("/query_valid_items/")
async def read_items(
    q: Optional[List[str]] = Query(
        None, min_length=3, max_length=50, regex="^fixedquery$", alias="query-item"
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# validation for path parameters
# ... means a value is required (no defaults)
@app.get("/path_valid_items/{item_id}")
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get", ge=1, le=5),
    q: Optional[str] = Query(None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# a mixed example
@app.put("/body_items_mix/{item_id}")
async def update_item(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    q: Optional[str] = None,
    item: Optional[BodyItem] = Body(None, example={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
            "tags": ["blue", "blue", "large"]
        }),
    user: BodyUser,
    importance: int = Body(..., gt=0, embed=False)
):
    results = {"item_id": item_id, "user": user}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


# a deeply nested example
# everything has editor support
class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()
    images: Optional[List[Image]] = None

class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: List[Item]

@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    return images


# Pydantic model subclassing to reduce code duplication
# subclassed classes only need to contain the difference with base
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


# use Dict[] when not sure about the request parameters
@app.get("/keyword-weights/", response_model=Dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}

