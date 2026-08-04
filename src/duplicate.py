from PIL import Image
import imagehash

class DuplicateDetector:

    def __init__(self, threshold=5):
        self.threshold = threshold
    def compute_hash(self, image_path):
        image = Image.open(image_path)
        return imagehash.phash(image)
    def find_duplicates(self, image_paths):
        duplicates = []
        hashes = {}
        for image in image_paths:
            current_hash = self.compute_hash(image)
            is_duplicate = False
            for previous_hash, previous_image in hashes.items():
                distance = current_hash - previous_hash
                if distance <= self.threshold:
                    duplicates.append(
                    (
                        previous_image,
                        image,
                        distance
                    )
                )
                    is_duplicate = True
                    break
            if not is_duplicate:
                hashes[current_hash] = image    
        return duplicates

    

    
