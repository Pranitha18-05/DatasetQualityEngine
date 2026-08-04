import cv2
import numpy as np
import matplotlib.pyplot as plt

class BrightnessAnalyzer:

    def __init__(self, dark_threshold=50, bright_threshold=200):
        self.dark_threshold = dark_threshold
        self.bright_threshold = bright_threshold
    def calculate_brightness(self, image_path):

        image = cv2.imread(str(image_path))

        if image is None:
            raise ValueError(
            f"Unable to load image: {image_path}")

        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

        brightness = np.mean(gray)

        return brightness
    def classify(self, brightness):
        if brightness < self.dark_threshold:
                return "Too Dark"
        
        elif brightness > self.bright_threshold:
            return "Too Bright"
        
        else:
            return "Normal"
    def plot_histogram(self, image_path):
         image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
         hist = cv2.calcHist([image],[0],None,[256],[0, 256])
         plt.figure(figsize=(8,4))
         plt.plot(hist)
         plt.title("Brightness Histogram")
         plt.xlabel("Pixel Intensity")
         plt.ylabel("Number of Pixels")
         plt.grid(True)
         plt.show()
         plt.savefig(f"reports/{image_path.stem}_histogram.png")
         plt.close()

