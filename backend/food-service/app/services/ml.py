import io
import json
import logging
from typing import Any, Dict, List
import numpy as np
from PIL import Image
from app.core.config import settings

logger = logging.getLogger("food_service.ml")

_model = None
_class_names: List[str] | None = None
IMG_SIZE = 224


def get_class_names() -> List[str]:
    global _class_names
    if _class_names is None:
        class_names_path = settings.get_effective_class_names_path()
        if not class_names_path.exists():
            raise FileNotFoundError(f"class_names.json not found at {class_names_path}")
        with open(class_names_path, "r", encoding="utf-8") as f:
            _class_names = json.load(f)
        logger.info(f"Loaded {len(_class_names)} food class names.")
    return _class_names


def get_model():
    global _model
    if _model is None:
        import tensorflow as tf

        model_path = settings.get_effective_model_path()
        if not model_path.exists():
            raise FileNotFoundError(f"Keras model not found at {model_path}")
        logger.info(f"Loading Keras model from {model_path}...")
        _model = tf.keras.models.load_model(str(model_path))
        logger.info("Keras model loaded successfully.")
    return _model


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((IMG_SIZE, IMG_SIZE))
    img_array = np.array(img, dtype=np.float32)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def predict_food_labels(image_bytes: bytes, top_k: int = 1) -> List[Dict[str, Any]]:
    model = get_model()
    class_names = get_class_names()

    if not (1 <= top_k <= len(class_names)):
        top_k = 1

    img_tensor = preprocess_image(image_bytes)
    preds = model.predict(img_tensor, verbose=0)[0]
    top_indices = np.argsort(preds)[::-1][:top_k]

    results = [
        {
            "rank": int(i + 1),
            "label": class_names[idx],
            "confidence": round(float(preds[idx]) * 100, 2),
        }
        for i, idx in enumerate(top_indices)
    ]
    return results
