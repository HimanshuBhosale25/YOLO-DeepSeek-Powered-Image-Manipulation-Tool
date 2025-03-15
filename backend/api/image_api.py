from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Response
from typing import Annotated
from PIL import Image
import io
from image_processing import adjustments
from llm_integration.llm_client import GroqClient
import os
from ultralytics import YOLO
import cv2
import numpy as np
import uuid
import time 
from scipy.ndimage import gaussian_filter

router = APIRouter()

yolo_model = YOLO('yolov8l-seg.pt')

sessions = {}
SESSION_TIMEOUT = 3600  

def cleanup_sessions():
    current_time = time.time()
    expired_sessions = [session_id for session_id, session_data in sessions.items() if current_time - session_data["last_access"] > SESSION_TIMEOUT]
    for session_id in expired_sessions:
        del sessions[session_id]

def detect_objects(image_cv2, target_class, conf_threshold=0.25, iou_threshold=0.45):
    try:
        results = yolo_model(cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB), conf=conf_threshold, iou=iou_threshold)
        detected_masks = []
        for result in results:
            if result.masks is not None:
                class_ids = result.boxes.cls.cpu().numpy()
                masks = result.masks.data.cpu().numpy()
                for class_id, mask in zip(class_ids, masks):
                    if yolo_model.names[int(class_id)] == target_class:
                        detected_masks.append(mask)
        return detected_masks
    except Exception as e:
        print(f"Error in detect_objects: {e}")
        return []

def refine_mask(mask):
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)
    return mask

def process_mask(image_cv2, mask):
    mask_resized = cv2.resize((mask * 255).astype(np.uint8), (image_cv2.shape[1], image_cv2.shape[0]))
    mask_refined = refine_mask(mask_resized)
    mask_blurred = cv2.GaussianBlur(mask_refined, (15, 15), 0)
    return mask_blurred

@router.post("/create_session/")
async def create_session(file: UploadFile = File(...)):
    session_id = str(uuid.uuid4())
    contents = await file.read()
    sessions[session_id] = {"image_data": contents, "last_access": time.time()}
    return {"session_id": session_id}

@router.post("/process_all_adjustments/")
async def process_all_adjustments(
    session_id: Annotated[str, Form()],
    prompt: Annotated[str, Form()],
):
    cleanup_sessions()
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found.")
    sessions[session_id]["last_access"] = time.time()
    session = sessions[session_id]
    image_data = session["image_data"]

    try:
        image_cv2 = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
        image_pil = Image.fromarray(cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB))

        groq_client = GroqClient(api_key=os.environ.get("GROQ_API_KEY"))
        adjustment_factors_list = groq_client.generate_text(prompt)

        if not adjustment_factors_list or "edits" not in adjustment_factors_list:
            raise HTTPException(status_code=400, detail="Failed to get adjustment factors.")

        masks = detect_objects(image_cv2.copy(), "person")
        mask = None
        if masks:
            mask = masks[0]
            mask_blurred = process_mask(image_cv2.copy(), mask)
            mask_blurred_uint8 = mask_blurred.astype(np.uint8)
            background_mask = 255 - mask_blurred_uint8
            mask_3channel = np.stack([mask_blurred_uint8] * 3, axis=-1) / 255.0
            background_mask_3channel = np.stack([background_mask] * 3, axis=-1) / 255.0

        for adjustment_factors in adjustment_factors_list["edits"]:
            target_area = adjustment_factors.get("target_area", "object")

            if target_area == "global":
                adjusted_pil = Image.fromarray(cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB))
                adjusted_pil = adjustments.adjust_contrast(adjusted_pil, adjustment_factors.get("contrast", 1.0))
                adjusted_pil = adjustments.adjust_exposure(adjusted_pil, adjustment_factors.get("exposure", 1.0))
                if adjustment_factors.get("sharpen", False):
                    adjusted_pil = adjustments.sharpen_image(adjusted_pil)
                if "red_tint" in adjustment_factors:
                    adjusted_pil = adjustments.add_color_tint(adjusted_pil, adjustment_factors.get("red_tint", 0), adjustment_factors.get("green_tint", 0), adjustment_factors.get("blue_tint", 0))
                image_cv2 = cv2.cvtColor(np.array(adjusted_pil), cv2.COLOR_RGB2BGR)

            elif target_area == "object":
                if mask is None:
                    raise HTTPException(status_code=404, detail=f"No person found.")
                adjusted_pil = Image.fromarray(cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB))
                adjusted_pil = adjustments.adjust_saturation(adjusted_pil, adjustment_factors.get("saturation", 1.0))
                adjusted_pil = adjustments.adjust_contrast(adjusted_pil, adjustment_factors.get("contrast", 1.0))
                adjusted_pil = adjustments.adjust_exposure(adjusted_pil, adjustment_factors.get("exposure", 1.0))
                image_object_adjusted = cv2.cvtColor(np.array(adjusted_pil), cv2.COLOR_RGB2BGR)
                image_cv2 = (image_cv2 * (1 - mask_3channel) + image_object_adjusted * mask_3channel).astype(np.uint8)

            elif target_area == "background":
                if mask is None:
                    raise HTTPException(status_code=404, detail=f"No person found.")
                adjusted_pil = Image.fromarray(cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB))
                if "grayscale" in adjustment_factors and adjustment_factors.get("grayscale", False):
                    adjusted_pil = adjustments.grayscale_image(adjusted_pil)
                if "saturation" in adjustment_factors:
                    adjusted_pil = adjustments.adjust_saturation(adjusted_pil, adjustment_factors.get("saturation", 1.0))
                if "contrast" in adjustment_factors:
                    adjusted_pil = adjustments.adjust_contrast(adjusted_pil, adjustment_factors.get("contrast", 1.0))
                if "exposure" in adjustment_factors:
                    adjusted_pil = adjustments.adjust_exposure(adjusted_pil, adjustment_factors.get("exposure", 1.0))
                if "hue" in adjustment_factors:
                    adjusted_pil = adjustments.adjust_hue(adjusted_pil, adjustment_factors.get("hue", 0.0))
                if "red_factor" in adjustment_factors and "green_factor" in adjustment_factors and "blue_factor" in adjustment_factors:
                    adjusted_pil = adjustments.adjust_color_factors(adjusted_pil, adjustment_factors.get("red_factor", 1.0), adjustment_factors.get("green_factor", 1.0), adjustment_factors.get("blue_factor", 1.0))
                if "vignette" in adjustment_factors:
                    adjusted_pil = adjustments.add_vignette(adjusted_pil, adjustment_factors.get("vignette", 0.0))
                if "noise" in adjustment_factors:
                    adjusted_pil = adjustments.add_noise(adjusted_pil, adjustment_factors.get("noise", 0))
                if "black_point" in adjustment_factors:
                    adjusted_pil = adjustments.adjust_levels(adjusted_pil, adjustment_factors.get("black_point", 0), adjustment_factors.get("white_point", 255), adjustment_factors.get("midtones", 1.0))
                if "red_tint" in adjustment_factors:
                    adjusted_pil = adjustments.add_color_tint(adjusted_pil, adjustment_factors.get("red_tint", 0), adjustment_factors.get("green_tint", 0), adjustment_factors.get("blue_tint", 0))
                if "sharpen" in adjustment_factors and adjustment_factors.get("sharpen", False):
                    adjusted_pil = adjustments.sharpen_image(adjusted_pil)
                if "blur" in adjustment_factors and adjustment_factors.get("blur", False):
                    adjusted_pil = adjustments.blur_image(adjusted_pil)
                if "invert" in adjustment_factors and adjustment_factors.get("invert", False):
                    adjusted_pil = adjustments.invert_colors(adjusted_pil)
                image_background_adjusted = cv2.cvtColor(np.array(adjusted_pil), cv2.COLOR_RGB2BGR)
                image_cv2 = (image_cv2 * (1 - background_mask_3channel) + image_background_adjusted * background_mask_3channel).astype(np.uint8)

        modified_image_pil = Image.fromarray(cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB))
        modified_image_buffer = io.BytesIO()
        modified_image_pil.save(modified_image_buffer, format="PNG", optimize=True)
        modified_image_data = modified_image_buffer.getvalue()

        sessions[session_id]["image_data"] = modified_image_data
        return Response(content=modified_image_data, media_type="image/png")

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")