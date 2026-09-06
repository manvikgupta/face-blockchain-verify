import hashlib
import json

def generate_fingerprint(search_result: dict, image_hash: str):
    """
    Builds a canonical JSON record from search result + image hash,
    and SHA-256 hashes it.
    Returns a tuple of (fingerprint_hex, canonical_json_string).
    """
    record = {
        "image_hash": image_hash,
        "search_match": search_result
    }
    
    # Canonical JSON string (sorted keys, no spaces between separators)
    canonical_json = json.dumps(record, sort_keys=True, separators=(',', ':'))
    
    # SHA-256 hash
    fingerprint = hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()
    return fingerprint, canonical_json

def get_image_hash(image_path: str) -> str:
    """Computes SHA-256 hash of the local image file."""
    sha256_hash = hashlib.sha256()
    with open(image_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
