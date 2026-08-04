from cleaner import DatasetCleaner
from loader import ImageLoader

loader = ImageLoader("dataset/raw")

cleaner = DatasetCleaner()

images = loader.find_images()

clean, rejected = cleaner.clean_dataset(images)

print(f"Clean Images     : {clean}")

print(f"Rejected Images  : {rejected}")