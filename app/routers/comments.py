from fastapi import APIRouter

router = APIRouter(tags=["comments"])

@router.post("/shanyraks/{id}/comments")
def create_comment(id: int):
    return {"message": "Comment created"}

@router.get("/shanyraks/{id}/comments")
def get_comments(id: int):
    return {"comments": []}

@router.patch("/shanyraks/{id}/comments/{comment_id}")
def update_comment(id: int, comment_id: int):
    return {"message": "Comment updated"}

@router.delete("/shanyraks/{id}/comments/{comment_id}")
def delete_comment(id: int, comment_id: int):
    return {"message": "Comment deleted"}
