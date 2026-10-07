from pathlib import Path

import numpy as np
from PIL import Image

from src.gradcam import (
    CLASS_NAMES,
    create_overlay,
    generate_gradcam,
)


SAMPLE_IMAGE = Path(__file__).resolve().parents[1] / "assets" / "Image1.png"


def test_gradcam_generation():
    with Image.open(SAMPLE_IMAGE) as image:
        heatmap, predicted_class, confidence = generate_gradcam(image)

    assert heatmap.shape == (224, 224)
    assert np.isfinite(heatmap).all()
    assert 0.0 <= float(heatmap.min()) <= 1.0
    assert 0.0 <= float(heatmap.max()) <= 1.0

    assert predicted_class in range(len(CLASS_NAMES))
    assert 0.0 <= confidence <= 1.0


def test_gradcam_overlay():
    with Image.open(SAMPLE_IMAGE) as image:
        heatmap, _, _ = generate_gradcam(image)
        overlay = create_overlay(image, heatmap)

    assert overlay.size == (224, 224)
    assert overlay.mode == "RGB"
