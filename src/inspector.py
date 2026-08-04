from pathlib import Path

class DatasetInspector:

    def __init__(self, dataset_path):

        self.dataset_path = Path(dataset_path)
    def dataset_exists(self):

        return self.dataset_path.exists()
    def detect_dataset_type(self):

        images_folder = self.dataset_path / "images"

        labels_folder = self.dataset_path / "labels"

        image_extensions = [".jpg",".jpeg",".png",".bmp",".tif",".tiff"]

        if images_folder.exists() and labels_folder.exists():

            return "YOLO Dataset"

        subfolders = []

        for item in self.dataset_path.iterdir():

            if item.is_dir():

                subfolders.append(item)

        for folder in subfolders:

            for file in folder.iterdir():

                if file.suffix.lower() in image_extensions:

                    return "Classification Dataset"

        for file in self.dataset_path.iterdir():

                if file.suffix.lower() in image_extensions:

                    return "Image Dataset"
        return "Unknown Dataset"

    def inspect(self):

        dataset_type = self.detect_dataset_type()

        if dataset_type == "Classification Dataset":

            class_folders = []

            for item in self.dataset_path.iterdir():

                if item.is_dir():

                    class_folders.append(item)

            total_classes = len(class_folders)

            class_names = []

            total_images = 0

            class_distribution = {}

            image_extensions = [".jpg",".jpeg",".png",".bmp",".tif",".tiff"]

            for folder in class_folders:

                class_names.append(folder.name)

                image_count = 0

                for file in folder.iterdir():

                    if file.suffix.lower() in image_extensions:

                        image_count += 1

                        total_images += 1

                class_distribution[folder.name] = image_count

            average_images = total_images / total_classes

            distribution_percentages = {}

            for class_name, count in class_distribution.items():

                percentage = (count / total_images) * 100

                distribution_percentages[class_name] = percentage

            balanced = True

            for count in class_distribution.values():

                difference = abs(count - average_images)

                if difference > average_images * 0.20:

                    balanced = False

                    break

            if balanced:

                dataset_status = "Balanced"

            else:

                dataset_status = "Imbalanced"

            return {

    "dataset_type": dataset_type,

    "total_classes": total_classes,

    "class_names": class_names,

    "total_images": total_images,

    "average_images": average_images,

    "class_distribution": class_distribution,

    "distribution_percentages": distribution_percentages,

    "dataset_status": dataset_status,

    "annotation_audit": "Skipped"

}