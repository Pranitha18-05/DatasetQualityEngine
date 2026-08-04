import cv2
class BlurDetector:

    def __init__(self, threshold=100):
        self.threshold = threshold
    def calculate_blur(self, image_path):

        image = cv2.imread(str(image_path))

        if image is None:
            raise ValueError(
            f"Unable to load image: {image_path}")

        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

        laplacian = cv2.Laplacian(gray,cv2.CV_64F)

        score = laplacian.var()

        return score
    def classify(self, score):

        if score < self.threshold:
            return "Blurry"

        return "Sharp"