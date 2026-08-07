from pathlib import Path
from src.inspector import DatasetInspector


class LabelChecker:

    def __init__(self, dataset_path):
        self.dataset_path = Path(dataset_path)

    def find_missing_labels(self):
        inspector = DatasetInspector(self.dataset_path)
        dataset_type = inspector.detect_dataset_type()

        if dataset_type != "YOLO Dataset":
            return {
                "status": "Skipped",
                "reason": "Dataset is not a YOLO dataset.",
                "missing_labels": []
            }

        # DYNAMIC PATH FIX: 
        # If dataset_path ends with 'raw', shift focus up to the root project level
        base_dir = self.dataset_path if self.dataset_path.name != "raw" else self.dataset_path.parent
        
        images_root = base_dir / "images"
        labels_root = base_dir / "labels"

        missing_labels = []
        splits = ["train", "valid", "test"]
        image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"]

        for split in splits:
            image_folder = images_root / split
            label_folder = labels_root / split

            if not image_folder.exists():
                continue

            for image in image_folder.iterdir():
                if image.suffix.lower() not in image_extensions:
                    continue

                label_file = label_folder / f"{image.stem}.txt"

                if not label_file.exists():
                    # Logs with split prefix for clear tracking e.g. 'train/img1.jpg'
                    missing_labels.append(f"{split}/{image.name}")

        return {
            "status": "Completed",
            "missing_labels": missing_labels
        }
