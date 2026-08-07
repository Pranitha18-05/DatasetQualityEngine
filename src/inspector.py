from pathlib import Path

class DatasetInspector:

    def __init__(self, dataset_path):
        self.dataset_path = Path(dataset_path)

    def dataset_exists(self):
        return self.dataset_path.exists()

    def detect_dataset_type(self):
        # 1. Dynamic YOLO layout detection
        # Checks both inside 'dataset_path' or up one folder layer if targeting a subfolder like 'raw'
        base_dir = self.dataset_path if self.dataset_path.name != "raw" else self.dataset_path.parent
        if (base_dir / "images").exists() and (base_dir / "labels").exists():
            return "YOLO Dataset"

        image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"]

        # 2. Classification structure check
        if self.dataset_path.exists():
            for item in self.dataset_path.iterdir():
                # Filter out environment subdirectories and internal system paths
                if item.is_dir() and item.name not in [".venv", "__pycache__", "reports"]:
                    for file in item.iterdir():
                        if file.suffix.lower() in image_extensions:
                            return "Classification Dataset"

        # 3. Flat Image Collection structure check
        if self.dataset_path.exists():
            for file in self.dataset_path.iterdir():
                if file.suffix.lower() in image_extensions:
                    return "Image Dataset"

        return "Unknown Dataset"

    def inspect(self):
        dataset_type = self.detect_dataset_type()
        image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"]

        if dataset_type == "Classification Dataset":
            class_folders = [
                item for item in self.dataset_path.iterdir() 
                if item.is_dir() and item.name not in [".venv", "__pycache__", "reports"]
            ]
            total_classes = len(class_folders)
            class_names = []
            total_images = 0
            class_distribution = {}

            for folder in class_folders:
                class_names.append(folder.name)
                image_count = sum(1 for file in folder.iterdir() if file.suffix.lower() in image_extensions)
                total_images += image_count
                class_distribution[folder.name] = image_count

            # Safely catch empty folder configurations
            average_images = total_images / total_classes if total_classes > 0 else 0
            
            distribution_percentages = {
                class_name: (count / total_images) * 100 if total_images > 0 else 0 
                for class_name, count in class_distribution.items()
            }

            balanced = True
            for count in class_distribution.values():
                if average_images > 0 and abs(count - average_images) > average_images * 0.20:
                    balanced = False
                    break

            return {
                "dataset_type": dataset_type,
                "total_classes": total_classes,
                "class_names": class_names,
                "total_images": total_images,
                "average_images": average_images,
                "class_distribution": class_distribution,
                "distribution_percentages": distribution_percentages,
                "dataset_status": "Balanced" if balanced else "Imbalanced",
                "annotation_audit": "Skipped"
            }

        # Fallback return dictionary for Image Datasets or YOLO configurations
        # This completely guarantees your code never throws a NoneType loop exception
        total_imgs = sum(1 for file in self.dataset_path.rglob("*") if file.suffix.lower() in image_extensions)
        return {
            "dataset_type": dataset_type,
            "total_classes": 0,
            "class_names": [],
            "total_images": total_imgs,
            "average_images": total_imgs,
            "class_distribution": {},
            "distribution_percentages": {},
            "dataset_status": "N/A",
            "annotation_audit": "Pending" if dataset_type == "YOLO Dataset" else "Skipped"
        }
