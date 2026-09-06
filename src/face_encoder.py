import cv2
from deepface import DeepFace

def encode_face(image_path: str) -> list:
    """
    Detects and encodes a face from the given image path.
    Returns the facial embedding vector.
    Raises ValueError if no face is detected.
    """
    try:
        # DeepFace.represent returns a list of representations (one for each face)
        # We take the first one. Enforce detection ensures it fails if no face is found.
        embedding_objs = DeepFace.represent(img_path=image_path, model_name="Facenet", enforce_detection=True)
        if not embedding_objs:
            raise ValueError("No face detected in the image.")
        return embedding_objs[0]["embedding"]
    except Exception as e:
        raise ValueError(f"Error encoding face (ensure the image has a visible face): {e}")
