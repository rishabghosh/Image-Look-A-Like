from PIL import Image
import imagehash

# Replace these paths with two actual images you want to compare
img1_path = "./input/cartoon/1.png"
img2_path = "./input/cartoon/1.png"

hash1 = imagehash.average_hash(Image.open(img1_path))
hash2 = imagehash.average_hash(Image.open(img2_path))

distance = hash1 - hash2
print(f"Hash distance between {img1_path} and {img2_path}: {distance}")

if distance < 20:
    print("✅ Likely a match")
else:
    print("❌ Too different")
