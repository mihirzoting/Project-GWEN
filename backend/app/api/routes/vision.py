from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel


router = APIRouter()


class VisionCaptureRequest(BaseModel):
    session_id: str


class VisionCaptureResponse(BaseModel):
    status: str
    context: str


@router.post('/vision/capture', response_model=VisionCaptureResponse)
async def capture(payload: VisionCaptureRequest, request: Request) -> VisionCaptureResponse:
    vision_service = request.app.state.vision_service
    context = await vision_service.capture_and_extract(payload.session_id)
    return VisionCaptureResponse(status='ok', context=context)
