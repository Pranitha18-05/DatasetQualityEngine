from src.loader import ImageLoader
from src.blur import BlurDetector
from src.brightness import BrightnessAnalyzer
from src.resolution import ResolutionChecker
from src.statistics import DatasetStatistics
from src.cleaner import DatasetCleaner
from src.quality import QualityScorer
from src.inspector import DatasetInspector
from src.label_checker import LabelChecker
from src.empty_label_checker import EmptyLabelChecker
from src.bounding_box_validator import BoundingBoxValidator
from src.logger import logger
from pathlib import Path
from tqdm import tqdm

class DatasetPipeline:

    def __init__(self, dataset_path):
        # Ensure it's a Path object
        self.dataset_path = Path(dataset_path)

        self.loader = ImageLoader(self.dataset_path)
        self.blur = BlurDetector()
        self.brightness = BrightnessAnalyzer()
        self.resolution = ResolutionChecker()
        self.statistics = DatasetStatistics()
        self.cleaner = DatasetCleaner()
        self.quality = QualityScorer()
        
        # Dynamically set clean path at the same level as input folder
        # e.g., if input is 'dataset/raw', clean becomes 'dataset/clean'
        self.clean_dir = self.dataset_path.parent / "clean"

    def run(self):
        logger.info("Pipeline started")

        inspector = DatasetInspector(self.dataset_path)
        dataset_type = inspector.detect_dataset_type()

        print("=" * 50)
        print("DATASET INSPECTION")
        print("=" * 50)
        print(f"Dataset Type : {dataset_type}")
        print("=" * 50)

        images = self.loader.find_images()
        logger.info(f"Total images found: {len(images)}")
        
        # FIX: Pass self.dataset_path so cleaner knows the root structure
        clean_count, rejected_count = self.cleaner.clean_dataset(images, root_path=self.dataset_path)
        
        print("\n===== CLEANING SUMMARY =====")
        print(f"Clean Images     : {clean_count}")
        print(f"Rejected Images  : {rejected_count}")
        
        # FIX: Dynamically load from the clean directory instead of a hardcoded string
        clean_loader = ImageLoader(self.clean_dir)
        images = clean_loader.find_images()

        for image in tqdm(images, desc="Processing Images", unit="image"):
            blur_score = self.blur.calculate_blur(image)
            blur_status = self.blur.classify(blur_score)

            brightness_value = self.brightness.calculate_brightness(image)
            brightness_status = self.brightness.classify(brightness_value)

            width, height = self.resolution.get_resolution(image)
            resolution_status = self.resolution.classify(width, height)

            quality_score = self.quality.calculate_score(blur_status, brightness_status, resolution_status)
            quality_category = self.quality.get_category(quality_score)

            # To keep subfolder tracking in stats, log the relative path instead of just image.name
            relative_name = image.relative_to(self.clean_dir)

            self.statistics.add_record(
                filename=str(relative_name),  # Saves as 'good/img1.jpg' instead of 'img1.jpg'
                blur_score=blur_score,
                blur_status=blur_status,
                brightness=brightness_value,
                brightness_status=brightness_status,
                width=width,
                height=height,
                resolution_status=resolution_status,
                quality_score=quality_score,
                quality_category=quality_category
            )

        self.statistics.save_report()
        self.statistics.save_quality_report()
        self.statistics.plot_quality_distribution()
        self.statistics.print_summary()

        logger.info("Quality report generated")

        if dataset_type == "YOLO Dataset":
            print("\nRunning Annotation Audit...\n")
            label_checker = LabelChecker(self.dataset_path)
            missing = label_checker.find_missing_labels()
            print(missing)

            empty_checker = EmptyLabelChecker(self.dataset_path)
            empty = empty_checker.find_empty_labels()
            print(empty)

            bbox = BoundingBoxValidator(self.dataset_path.parent, num_classes=3)
            result = bbox.validate()
            print(result)
        else:
            print()
            print("Annotation Audit Skipped")
            print("Reason : Dataset is not a YOLO dataset.")

        logger.info("Pipeline completed successfully")
