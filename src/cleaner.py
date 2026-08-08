from pathlib import Path
from PIL import Image
import shutil
import pandas as pd

class DatasetCleaner:

    def __init__(self):
        # We will initialize paths dynamically inside clean_dataset
        self.clean_folder = None
        self.rejected_folder = None

    def check_image(self, image_path):
        try:
            with Image.open(image_path) as img:
                img.load()
            return True
        except Exception:
            return False
        
    def copy_clean(self, image_path, relative_path):
        destination = self.clean_folder / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True) # Create subfolder if needed
        shutil.copy2(image_path, destination)

    def copy_rejected(self, image_path, relative_path):
        destination = self.rejected_folder / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True) # Create subfolder if needed
        # CHANGED: Use copy2 instead of move so your raw folder stays safe and untouched!
        shutil.copy2(image_path, destination)

    def clean_dataset(self, image_paths, root_path):
        # 1. Fallback folder fallback rules if the pipeline didn't override them
        if not self.clean_folder:
            root_path = Path(root_path)
            self.clean_folder = root_path.parent / "clean"
            self.rejected_folder = root_path.parent / "rejected"
        
        # Ensure base output directories physically exist
        self.clean_folder.mkdir(parents=True, exist_ok=True)
        self.rejected_folder.mkdir(parents=True, exist_ok=True)
        
        self.reset_folders()
        clean = 0
        rejected = 0
        rows = []
        
        # Ensure root_path is a Path object for comparison
        root_path = Path(root_path)
        
        for image in image_paths:
            # 🛠️ FIXED PATH ANCHOR FALLBACK: Handles any dynamic/cloud path configuration safely!
            try:
                # First try resolving relative to the passed root path
                relative_path = image.relative_to(root_path)
            except ValueError:
                # If that fails (like in cloud mode), check if there are category subfolders
                # by looking at the parent folder name (e.g., 'good' or 'bad')
                if image.parent.name in ["good", "bad"] or (image.parent != image.parents[-1] and image.parent.name != "uploads"):
                    relative_path = Path(image.parent.name) / image.name
                else:
                    relative_path = Path(image.name)
            
            if self.check_image(image):
                self.copy_clean(image, relative_path)
                rows.append({"Filename": str(relative_path), "Status": "Clean", "Reason": "Valid Image"})
                clean += 1
            else:
                self.copy_rejected(image, relative_path)
                rows.append({"Filename": str(relative_path), "Status": "Rejected", "Reason": "Corrupted Image"})
                rejected += 1
                
        # Ensure reports folder exists before saving csv
        Path("reports").mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame(rows)
        df.to_csv("reports/cleaning_report.csv", index=False)
        return clean, rejected

    def reset_folders(self):
        # Safely clear out existing old runs recursively if folders have items
        if self.clean_folder.exists():
            shutil.rmtree(self.clean_folder)
        if self.rejected_folder.exists():
            shutil.rmtree(self.rejected_folder)
            
        self.clean_folder.mkdir(parents=True, exist_ok=True)
        self.rejected_folder.mkdir(parents=True, exist_ok=True)
