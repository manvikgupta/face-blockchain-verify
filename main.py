import os
import sys
import json
from src.pipeline import run_pipeline
from src import fingerprint, blockchain

# Ensure paths are correct
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verify_record(tamper=False):
    if not os.path.exists("latest_record.json"):
        print("No latest_record.json found. Run the full pipeline first.")
        return

    with open("latest_record.json", "r") as f:
        data = json.load(f)

    image_path = data["image_path"]
    clean_result = data["clean_result"]
    record_id = data["record_id"]

    if tamper:
        print("\n--- Tampering with content ---")
        clean_result["title"] = "TAMPERED FAKE TITLE"

    try:
        img_hash = fingerprint.get_image_hash(image_path)
        fp_hex, _ = fingerprint.generate_fingerprint(clean_result, img_hash)
        
        print(f"Calculated hash : {fp_hex}")

        retrieved_hex = blockchain.get_record(record_id)
        retrieved_clean = retrieved_hex.replace('0x', '')
        print(f"Blockchain hash : {retrieved_clean}")
        print("")

        if retrieved_clean == fp_hex:
            print("[+] VERIFIED — CONTENT IS UNMODIFIED")
        else:
            print("[-] VERIFICATION FAILED — CONTENT HAS CHANGED")

    except Exception as e:
        print(f"Verification process encountered an error: {e}")


def main():
    print("==================================================================")
    print("WARNING: This tool is for verifying content about a CONSENTING subject")
    print("(e.g. the user's own face) only.")
    print("Do NOT use this to search for or identify non-consenting individuals.")
    print("==================================================================\n")

    while True:
        print("1. Run full pipeline")
        print("2. Verify blockchain record")
        print("3. Test tampered content")
        print("4. Exit")
        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            print("\nEnter image path (leave blank for sample image):")
            img_path = input("> ").strip()
            
            if not img_path:
                img_path = os.path.join("sample_data", "sample_face.jpg")
                img_url = "https://raw.githubusercontent.com/manvikgupta/face-blockchain-verify/main/sample_data/sample_face.jpg"
                print(f"Using default sample image: {img_path}")
            else:
                if not os.path.exists(img_path):
                    print(f"✗ File not found: {img_path}")
                    continue
                # For custom images, we need a public URL for reverse search
                print("\nEnter a PUBLICLY ACCESSIBLE URL for this exact image (for reverse image search):")
                img_url = input("> ").strip()
                if not img_url:
                    print("✗ Public URL is required for reverse image search.")
                    continue

            run_pipeline(img_path, img_url)

        elif choice == "2":
            verify_record(tamper=False)
        elif choice == "3":
            verify_record(tamper=True)
        elif choice == "4":
            break
        else:
            print("Invalid choice.")
        
        print("\n" + "-"*60 + "\n")

if __name__ == "__main__":
    main()