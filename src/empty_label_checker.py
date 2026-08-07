from pathlib import Path
from src.inspector import DatasetInspector


class EmptyLabelChecker:

    def __init__(self, dataset_path):
        self.dataset_path = Path(dataset_path)

    def find_empty_labels(self):
        inspector = DatasetInspector(self.dataset_path)

        if inspector.detect_dataset_type() != "YOLO Dataset":
            return {
                "status": "Skipped",
                "reason": "Dataset is not a YOLO dataset.",
                "empty_labels": []
            }

        # DYNAMIC PATH FIX: 
        # If dataset_path ends with 'raw', shift focus up to the root project level
        base_dir = self.dataset_path if self.dataset_path.name != "raw" else self.dataset_path.parent
        labels_root = base_dir / "labels"

        empty_files = []
        splits = ["train", "valid", "test"]

        for split in splits:
            label_folder = labels_root / split
            if not label_folder.exists():
                continue

            for label in label_folder.glob("*.txt"):
                # Check 1: Quick check if file size is 0 bytes
                if label.stat().st_size == 0:
                    empty_files.append(f"{split}/{label.name}")
                    continue
                
                # Check 2: Check if file contains only whitespaces or blank lines
                with open(label, "r", encoding="utf-8") as file:
                    content = file.read().strip()
                    if not content:
                        empty_files.append(f"{split}/{label.name}")

        return {
            "status": "Completed",
            "empty_labels": empty_files
        }
