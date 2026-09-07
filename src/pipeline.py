import os
import re
from . import face_encoder, image_search, face_matcher, fingerprint, blockchain

def extract_name_from_result(search_result: dict) -> str:
    """
    Attempts to extract a likely person's name from the matched post's title/snippet.
    This is a simple heuristic, not a guaranteed-accurate identification.
    """
    title = search_result.get("title", "") or ""
    snippet = search_result.get("snippet", "") or ""
    text = f"{title} {snippet}"

    # Common patterns: "Name - description", "Name | description", "Name's post"
    # Try splitting on common separators first
    for sep in [" - ", " | ", ": "]:
        if sep in title:
            candidate = title.split(sep)[0].strip()
            if 2 <= len(candidate.split()) <= 4:  # plausible name length
                return candidate

    # Fallback: look for capitalized word sequences (simple proper-noun heuristic)
    matches = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})\b', text)
    if matches:
        return matches[0]

    return "Unknown"

def run_pipeline(image_path: str, image_url: str):
    print("========================================================")
    print("     HH GOA 2026 — FACE & BLOCKCHAIN VERIFIER")
    print("========================================================")
    
    print("\n[1/7] Loading input image...")
    if not os.path.exists(image_path):
        print(f"      ✗ Image file not found at {image_path}")
        return
    print("      ✓ Image loaded")
        
    print("\n[2/7] Detecting and encoding face...")
    try:
        embedding = face_encoder.encode_face(image_path)
        print("      ✓ Face detected")
        print("      ✓ Face embedding generated")
    except Exception as e:
        safe_msg = str(e).encode('ascii', 'replace').decode('ascii')
        print(f"      ✗ Face encoding failed: {safe_msg}")
        return

    print("\n[3/7] Searching the web...")
    try:
        candidates = image_search.search_image(image_url)
        if candidates:
            print(f"      ✓ {len(candidates)} candidate results discovered")
        else:
            print("      ✗ No candidate results found.")
            return
    except Exception as e:
        print(f"      ✗ Web search failed: {e}")
        return

    try:
        best_match_info = face_matcher.find_best_match(embedding, candidates, threshold=0.60)
    except Exception as e:
        print(f"      ✗ Error during face matching: {e}")
        return

    print("\n[5/7] Match selected")
    if best_match_info:
        search_result = best_match_info["candidate"]
        identified_name = extract_name_from_result(search_result)
        print("      ✓ Matching post found")
        print(f"      Identified name (heuristic): {identified_name}")
        print(f"      URL: {search_result['post_url']}")
    else:
        print("      ✗ NO CONFIDENT MATCH FOUND")
        return

    print("\n[6/7] Creating fingerprint...")
    try:
        img_hash = fingerprint.get_image_hash(image_path)
        
        clean_result = {
            "post_url": search_result["post_url"],
            "title": search_result["title"],
            "source": search_result["source"],
            "identified_name": identified_name
        }
        fp_hex, canon_json = fingerprint.generate_fingerprint(clean_result, img_hash)
        print(f"      SHA-256: {fp_hex}")
        
        print("\n      Blockchain transaction:")
        record_id, tx_hash = blockchain.store_record_with_tx(fp_hex)
        print(f"      {tx_hash}")
        
        import json
        with open("latest_record.json", "w") as f:
            json.dump({
                "image_path": image_path,
                "clean_result": clean_result,
                "record_id": record_id
            }, f, indent=4)
            
    except Exception as e:
        print(f"      ✗ Fingerprinting or Blockchain upload failed: {e}")
        return
        
    print("\n[7/7] Re-verifying...")
    try:
        retrieved_hex = blockchain.get_record(record_id)
        retrieved_clean = retrieved_hex.replace('0x', '')
        if retrieved_clean == fp_hex:
            print("      ✓ Blockchain hash matches")
            print("\n========================================================")
            print("                    VERIFIED ✓")
            print(f"          Identified: {identified_name}")
            print("========================================================")
        else:
            print("      ✗ Blockchain hash DOES NOT match")
            print("\n========================================================")
            print("                VERIFICATION FAILED ✗")
            print("========================================================")
    except Exception as e:
        print(f"      ✗ Re-verification failed: {e}")
        return