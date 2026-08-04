from pathlib import Path

from inspector import DatasetInspector


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

        labels_root = self.dataset_path / "labels"

        empty_files = []

        splits = ["train", "valid", "test"]

        for split in splits:

            label_folder = labels_root / split

            if not label_folder.exists():

                continue

            for label in label_folder.glob("*.txt"):

                if label.stat().st_size == 0:

                    empty_files.append(label.name)

        return {

            "status": "Completed",

            "empty_labels": empty_files

        }