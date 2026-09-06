
import os
import sys
from src.pipeline import run_pipeline

# Ensure paths are correct
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("==================================================================")
    print("WARNING: This tool is for verifying content about a CONSENTING subject")
    print("(e.g. the user's own face) only.")
    print("Do NOT use this to search for or identify non-consenting individuals.")
    print("==================================================================\n")
    
    sample_img_path = os.path.join("sample_data", "sample_face.jpg")

    # Publicly accessible URL to the SAME image, needed for reverse image search.
    # Easiest option: push sample_data/sample_face.jpg to your GitHub repo and use its raw URL.
    sample_img_url = "https://raw.githubusercontent.com/YOUR_USERNAME/face-blockchain-verify/main/sample_data/sample_face.jpg"

    run_pipeline(sample_img_path, sample_img_url)

if __name__ == "__main__":
    main()