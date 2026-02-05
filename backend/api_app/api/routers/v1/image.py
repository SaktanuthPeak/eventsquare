from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import Optional
from loguru import logger

from api_app import schemas
from api_app.services.image_service import ImageService
from api_app.api.core.dependencies import get_current_user
from api_app.models.user_model import User

router = APIRouter(prefix="/images", tags=["Images"])


@router.post(
    "/upload",
    response_model=schemas.ImageUploadResponse,
    status_code=201,
    summary="Upload an image",
)
async def upload_image(
    file: UploadFile = File(..., description="Image file to upload"),
    event_id: Optional[str] = Query(
        None, description="Event ID to associate with the image"
    ),
    current_user: User = Depends(get_current_user),
):
    """
    Upload an image to GridFS.

    - **file**: The image file (jpeg, png, gif, webp)
    - **event_id**: Optional event ID to link the image to an event

    Returns the uploaded image details including file_id and document_id.
    """
    service = ImageService()
    try:
        return await service.upload_image(file, event_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error uploading image: {e}")
        raise HTTPException(status_code=500, detail=f"Error uploading image: {str(e)}")


@router.get("/{image_id}", response_class=StreamingResponse, summary="Get an image")
async def get_image(image_id: str):
    """
    Retrieve an image from GridFS by its document ID.

    - **image_id**: The Image document ID

    Returns the image file as a stream.
    """
    service = ImageService()
    try:
        return await service.get_image(image_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error retrieving image: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving image: {str(e)}")


@router.delete("/{image_id}", status_code=204, summary="Delete an image")
async def delete_image(image_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete an image from GridFS and the database.

    - **image_id**: The Image document ID

    Requires authentication.
    """
    service = ImageService()
    try:
        await service.delete_image(image_id)
        return {"message": "Image deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error deleting image: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting image: {str(e)}")
