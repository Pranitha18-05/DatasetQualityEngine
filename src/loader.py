from pathlib import Path
from PIL import Image

SUPPORTED_FORMATS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tiff",
    ".webp"
}

class ImageLoader:

    def __init__(self, dataset_path):
        self.dataset_path = Path(dataset_path)
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Folder '{self.dataset_path}' does not exist.")
    def find_images(self):
        images = []
        for file in self.dataset_path.rglob("*"):
            if not file.is_file():
                continue
            if file.suffix.lower() in SUPPORTED_FORMATS:
                images.append(file)
        return images
    def extract_metadata(self, image_path):
        with Image.open(image_path) as img:
            return {
            "filename": image_path.name,
            "width": img.width,
            "height": img.height,
            "mode": img.mode,
            "format": img.format
            }
    def validate_image(self, image_path):
        try:
            with Image.open(image_path) as img:
                img.verify()
            return True

        except Exception:
            return False
