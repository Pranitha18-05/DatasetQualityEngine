from pathlib import Path
from PIL import Image
import shutil
import pandas as pd

class DatasetCleaner:

    def __init__(self):

        self.clean_folder = Path("dataset/clean")

        self.rejected_folder = Path("dataset/rejected")

        self.clean_folder.mkdir(parents=True,exist_ok=True)

        self.rejected_folder.mkdir(parents=True,exist_ok=True)

    def check_image(self, image_path):

        try:
            with Image.open(image_path) as img:
                img.load()
            return True
        except Exception as e:
            return False
        
    def copy_clean(self, image_path):
        destination = self.clean_folder / image_path.name
        shutil.copy2(image_path,destination)

    def move_rejected(self, image_path):
        destination = self.rejected_folder / image_path.name
        shutil.move(image_path,destination)

    def clean_dataset(self, image_paths):
        self.reset_folders()
        clean = 0
        rejected = 0
        rows = []
        for image in image_paths:
            if self.check_image(image):
                self.copy_clean(image)
                rows.append({"Filename": image.name,"Status": "Clean","Reason": "Valid Image"})
                clean += 1
            else:
                self.move_rejected(image)
                rows.append({"Filename": image.name,"Status": "Rejected","Reason": "Corrupted Image"})
                rejected += 1
        df = pd.DataFrame(rows)
        df.to_csv("reports/cleaning_report.csv",index=False)
        return clean, rejected
    def reset_folders(self):
        for file in self.clean_folder.iterdir():
            if file.is_file():
                file.unlink()
        for file in self.rejected_folder.iterdir():
            if file.is_file():
                file.unlink()
