#Basic CRUD handling

#module imports using fastapi for RestAPI handling
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

#importing model schema for CRUD items
from models import Prompt, PromptUpdate

router = APIRouter()

#Create new item
@router.post("/", response_description="Create a new prompt", status_code=status.HTTP_201_CREATED, response_model=Prompt)
def create_prompt(request: Request, prompt: Prompt = Body(...)):
    prompt = jsonable_encoder(prompt)
    new_prompt = request.app.database["prompts"].insert_one(prompt)
    created_prompt = request.app.database["prompts"].find_one(
        {"_id": new_prompt.inserted_id}
    )

    return created_prompt

#Return full list of items
@router.get("/", response_description="List all prompts", response_model=List[Prompt])
def list_prompts(request: Request):
    prompts = list(request.app.database["prompts"].find(limit=100))
    return prompts

#List items based on id
@router.get("", response_description="Get a single prompt based on id", response_model=Prompt)
def find_prompt(id: str, request: Request):
    if(prompt := request.app.database["prompts"].find_one({"_id": id})) is not None:
        return prompt
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Prompt with ID {id} not found")

#Update an item
@router.put("/{id}", response_description="Update a Prompt", response_model=Prompt)
def update_prompt(id: str, request: Request, prompt: PromptUpdate = Body(...)):
    prompt = {k: v for k, in prompt.dict().items() if v is not None}
    if len(prompt) >= 1:
        update_result = request.app.database["prompts"].update_one(
            {"_id": id}, {"$set": prompt}
        )
        if update_request.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Prompt with ID {id} not found")
    if(
        existing_prompt := request.app.database["prompts"].find_one({"_id": id})
    )is not None:
        return existing_prompt
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Prompt with ID {id} not found")

#Delete item
@router.delete("/{id}", response_description="Delete a Prompt")
def delete_prompt(id: str, request: Request, response: Response):
    delete_result = request.app.database["prompts"].delete_one({"_id": id})

    if delete_result.deleted_count ==1: #Check if database is empy
        response.status_code = status.HTTP_204_NO_CONTENT
        return Response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Prompt with ID {id} not found")

#Delete all items
@router.delete("/", response_description="Delete all Prompts")
def delete_all(request: Request, response: Response):
    delete_result = request.app.database["prompts"].delete_many({})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Prompts not available")