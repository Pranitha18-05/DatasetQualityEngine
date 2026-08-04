from loader import ImageLoader
from blur import BlurDetector
from brightness import BrightnessAnalyzer
from resolution import ResolutionChecker
from statistics import DatasetStatistics
from cleaner import DatasetCleaner
from quality import QualityScorer
from inspector import DatasetInspector
from label_checker import LabelChecker
from empty_label_checker import EmptyLabelChecker
from bounding_box_validator import BoundingBoxValidator
from logger import logger

class DatasetPipeline:

    def __init__(self):

        self.loader = ImageLoader("dataset/raw")

        self.blur = BlurDetector()

        self.brightness = BrightnessAnalyzer()

        self.resolution = ResolutionChecker()

        self.statistics = DatasetStatistics()

        self.cleaner = DatasetCleaner()

        self.quality = QualityScorer()
    def run(self):
        logger.info("Pipeline started")

        inspector = DatasetInspector("dataset/raw")

        dataset_type = inspector.detect_dataset_type()

        print("=" * 50)

        print("DATASET INSPECTION")

        print("=" * 50)

        print(f"Dataset Type : {dataset_type}")

        print("=" * 50)

        images = self.loader.find_images()
        logger.info(f"Total images found: {len(images)}")
        clean_count, rejected_count = self.cleaner.clean_dataset(images)
        print("\n===== CLEANING SUMMARY =====")
        print(f"Clean Images     : {clean_count}")
        print(f"Rejected Images  : {rejected_count}")
        
        clean_loader = ImageLoader("dataset/clean")
        images = clean_loader.find_images()

        for image in images:

            blur_score = self.blur.calculate_blur(image)

            blur_status = self.blur.classify(blur_score)

            brightness_value = self.brightness.calculate_brightness(image)

            brightness_status = self.brightness.classify(brightness_value)

            width, height = self.resolution.get_resolution(image)

            resolution_status = self.resolution.classify(width, height)

            quality_score = self.quality.calculate_score(blur_status,brightness_status,resolution_status)
            quality_category = self.quality.get_category(quality_score)

            self.statistics.add_record(

        filename=image.name,

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

            label_checker = LabelChecker("dataset/raw")

            missing = label_checker.find_missing_labels()

            print(missing)

            empty_checker = EmptyLabelChecker("dataset/raw")

            empty = empty_checker.find_empty_labels()

            print(empty)

            bbox = BoundingBoxValidator(

        "dataset",

        num_classes=3

    )

            result = bbox.validate()

            print(result)

        else:

            print()

            print("Annotation Audit Skipped")

            print("Reason : Dataset is not a YOLO dataset.")

        logger.info("Pipeline completed successfully")
