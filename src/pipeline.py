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

    def __init__(self, dataset_path, output_root=None):
        # Ensure it's a Path object
        self.dataset_path = Path(dataset_path)

        self.loader = ImageLoader(self.dataset_path)
        self.blur = BlurDetector()
        self.brightness = BrightnessAnalyzer()
        self.resolution = ResolutionChecker()
        self.statistics = DatasetStatistics()
        self.cleaner = DatasetCleaner()
        self.quality = QualityScorer()
        
        # CLOUD-SAFE PATH SEPARATION
        if output_root:
            # Used by FastAPI: isolates outputs inside a specific job folder
            self.output_root = Path(output_root)
            self.clean_dir = self.output_root / "clean"
            self.is_cloud = True
        else:
            # Local CLI Fallback: keeps your current local terminal behavior working
            self.output_root = Path("reports")
            self.clean_dir = self.dataset_path.parent / "clean"
            self.is_cloud = False

    def run(self):
        logger.info("Pipeline started")

        inspector = DatasetInspector(self.dataset_path)
        dataset_type = inspector.detect_dataset_type()

        print("=" * 50)
        print("DATASET INSPECTION")
        print("=" * 50)
        print(f"Dataset Type : {dataset_type}")
        print("=" * 50)

        # 1. Dynamically gather all images inside the unzipped dataset path recursively
        images = self.loader.find_images()
        logger.info(f"Total images found: {len(images)}")

        if not images:
            logger.warning("No images found in the dataset to process.")
            return
        
        # 2. ENSURE OUTPUT DIRECTORY EXISTS
        self.clean_dir.mkdir(parents=True, exist_ok=True)

        # 3. RUN CLEANER 
        clean_count = 0
        rejected_count = 0
        
        # Explicitly assign the destination folders directly into the cleaner object
        self.cleaner.clean_folder = self.clean_dir
        if self.is_cloud:
            self.cleaner.rejected_folder = self.clean_dir.parent / "rejected"
        else:
            self.cleaner.rejected_folder = self.dataset_path.parent / "rejected"
            
        self.cleaner.rejected_folder.mkdir(parents=True, exist_ok=True)

        # 🛠️ DYNAMIC FIX: 
        # Pass self.clean_dir as the root_path anchor to bypass cleaner's hardcoded override logic
        clean_count, rejected_count = self.cleaner.clean_dataset(images, root_path=self.clean_dir)
        
        print("\n===== CLEANING SUMMARY =====")
        print(f"Clean Images     : {clean_count}")
        print(f"Rejected Images  : {rejected_count}")
        
        # 4. LOAD CLEANED IMAGES FOR QUALITY ANALYSIS
        clean_loader = ImageLoader(self.clean_dir)
        images = clean_loader.find_images()

        print(f"Analyzing {len(images)} clean images for quality reports...")

        for image in tqdm(images, desc="Processing Images", unit="image"):
            blur_score = self.blur.calculate_blur(image)
            blur_status = self.blur.classify(blur_score)

            brightness_value = self.brightness.calculate_brightness(image)
            brightness_status = self.brightness.classify(brightness_value)

            width, height = self.resolution.get_resolution(image)
            resolution_status = self.resolution.classify(width, height)

            quality_score = self.quality.calculate_score(blur_status, brightness_status, resolution_status)
            quality_category = self.quality.get_category(quality_score)

            relative_name = image.name

            self.statistics.add_record(
                filename=str(relative_name),
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
        print("\n SUCCESS: Pipeline reached the final line and completed successfully!")
