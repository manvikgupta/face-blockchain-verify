import os
from . import face_encoder, image_search, fingerprint, blockchain

def run_pipeline(image_path: str, image_url: str):
    """
    image_path: local path to the face image (used for face encoding + hashing)
    image_url: publicly accessible URL to the SAME image (used for reverse image search)
    """
    print("\n--- Face-Blockchain Verify Pipeline ---")
    
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        return
        
    print(f"\n[1/4] Encoding face from {image_path}...")
    try:
        embedding = face_encoder.encode_face(image_path)
        print(f"Face encoded successfully. Vector length: {len(embedding)}")
    except Exception as e:
        safe_msg = str(e).encode('ascii', 'replace').decode('ascii')
        print(f"Face encoding failed: {safe_msg}")
        return

    print(f"\n[2/4] Searching web for matches using {image_url}...")
    try:
        search_result = image_search.search_image(image_url)
        if search_result:
            print("Match found!")
            print(f"URL: {search_result['post_url']}")
            print(f"Title: {search_result['title']}")
        else:
            print("No matching web results found.")
            search_result = {"status": "no_match"}
    except Exception as e:
        print(f"Web search failed: {e}")
        return

    print("\n[3/4] Fingerprinting result...")
    try:
        img_hash = fingerprint.get_image_hash(image_path)
        fp_hex, canon_json = fingerprint.generate_fingerprint(search_result, img_hash)
        print(f"Canonical Record: {canon_json}")
        print(f"SHA-256 Fingerprint: {fp_hex}")
    except Exception as e:
        print(f"Fingerprinting failed: {e}")
        return
        
    print("\n[4/4] Uploading to blockchain...")
    try:
        record_id = blockchain.store_record(fp_hex)
        print(f"Record successfully stored on blockchain with ID: {record_id}")
    except Exception as e:
        print(f"Blockchain upload failed: {e}")
        return
        
    print("\n[5/5] Re-verifying from blockchain...")
    try:
        retrieved_hex = blockchain.get_record(record_id)
        retrieved_clean = retrieved_hex.replace('0x', '')
        if retrieved_clean == fp_hex:
            print("SUCCESS: Blockchain record matches local fingerprint!")
        else:
            print(f"FAILURE: Blockchain record ({retrieved_clean}) does not match local fingerprint ({fp_hex})!")
    except Exception as e:
        print(f"Re-verification failed: {e}")
        return