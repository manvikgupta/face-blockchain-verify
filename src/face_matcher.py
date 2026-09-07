import os
import math
import requests
import tempfile
from . import face_encoder

def cosine_similarity(v1, v2):
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_a = math.sqrt(sum(a * a for a in v1))
    norm_b = math.sqrt(sum(b * b for b in v2))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

def download_image(url: str, save_path: str) -> bool:
    try:
        # Use headers to avoid some basic blocks
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        resp = requests.get(url, stream=True, timeout=10, headers=headers)
        resp.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in resp.iter_content(1024):
                f.write(chunk)
        return True
    except Exception:
        return False

def find_best_match(input_embedding: list, candidates: list, threshold: float = 0.70):
    """
    Ranks candidates by face similarity and returns the best match if it exceeds the threshold.
    """
    print("\n[4/7] Comparing candidate faces...")
    
    ranked_candidates = []
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for i, candidate in enumerate(candidates):
            img_url = candidate.get("image_url")
            if not img_url or not img_url.startswith("http"):
                print(f"      Candidate {i+1}    - No valid image URL")
                continue
                
            temp_img_path = os.path.join(temp_dir, f"candidate_{i}.jpg")
            if not download_image(img_url, temp_img_path):
                print(f"      Candidate {i+1}    - Image download failed")
                continue
                
            try:
                # Encode face
                cand_embedding = face_encoder.encode_face(temp_img_path)
                sim = cosine_similarity(input_embedding, cand_embedding)
                
                ranked_candidates.append({
                    "candidate": candidate,
                    "similarity": sim
                })
                print(f"      Candidate {i+1}    {sim:.2f}")
            except Exception as e:
                # No face detected or other error
                print(f"      Candidate {i+1}    - No face detected")
                pass

    if not ranked_candidates:
        return None

    # Sort by similarity descending
    ranked_candidates.sort(key=lambda x: x["similarity"], reverse=True)
    best_match = ranked_candidates[0]
    
    if best_match["similarity"] >= threshold:
        # Re-print best match to highlight it as per CLI requirements
        print(f"      BEST MATCH: Candidate {candidates.index(best_match['candidate'])+1} with score {best_match['similarity']:.2f}")
        return best_match
    else:
        print(f"      Best match ({best_match['similarity']:.2f}) is below threshold ({threshold:.2f}).")
        return None
