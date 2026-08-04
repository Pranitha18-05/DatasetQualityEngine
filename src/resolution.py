import cv2
class ResolutionChecker:

    def __init__(
        self,
        min_width=300,
        min_height=300,
        max_width=4000,
        max_height=4000
    ):

        self.min_width = min_width
        self.min_height = min_height
        self.max_width = max_width
        self.max_height = max_height
    def get_resolution(self, image_path):
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Unable to load image: {image_path}")
        height, width = image.shape[:2]
        return width, height
    def calculate_aspect_ratio(self, width, height):
        return width / height
    def classify(self, width, height):
        if width < self.min_width or height < self.min_height:
            return "Too Small"
        elif width > self.max_width or height > self.max_height:
            return "Too Large"
        return "Normal"