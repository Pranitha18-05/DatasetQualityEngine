from pathlib import Path

from inspector import DatasetInspector


class BoundingBoxValidator:

    def __init__(self, dataset_path, num_classes):

        self.dataset_path = Path(dataset_path)

        self.num_classes = num_classes

    def validate(self):

        inspector = DatasetInspector(self.dataset_path)

        if inspector.detect_dataset_type() != "YOLO Dataset":

            return {
                "status": "Skipped",
                "reason": "Dataset is not a YOLO dataset.",
                "errors": []
            }

        labels_root = self.dataset_path / "labels"

        splits = ["train", "valid", "test"]

        errors = []

        for split in splits:

            label_folder = labels_root / split

            if not label_folder.exists():

                continue

            for label_file in label_folder.glob("*.txt"):

                with open(label_file, "r") as file:

                    for line_number, line in enumerate(file, start=1):

                        line = line.strip()

                        if not line:

                            continue

                        result = self.validate_line(line)

                        if result is not None:

                            errors.append({

                                "file": label_file.name,

                                "line": line_number,

                                "error": result

                            })

        return {

            "status": "Completed",

            "errors": errors

        }

    def validate_line(self, line):

        parts = line.split()

        if len(parts) != 5:

            return "Expected 5 values"

        try:
            class_id = int(parts[0])

            x = float(parts[1])

            y = float(parts[2])

            width = float(parts[3])

            height = float(parts[4])

        except ValueError:

            return "Non-numeric value"

        if class_id < 0 or class_id >= self.num_classes:

            return "Invalid class ID"

        if not (0 <= x <= 1):

            return "Center X out of range"

        if not (0 <= y <= 1):

            return "Center Y out of range"

        if not (0 < width <= 1):

            return "Invalid width"

        if not (0 < height <= 1):

            return "Invalid height"

        return None