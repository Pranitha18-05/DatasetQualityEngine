class QualityScorer:

    def __init__(self):

        pass
    def calculate_score(self,blur_status,brightness_status,resolution_status):
        score = 100
        if blur_status == "Blurry":
            score -= 20
        if brightness_status == "Too Dark":
            score -= 10
        elif brightness_status == "Too Bright":
            score -= 10
        if resolution_status == "Low Resolution":
            score -= 15
        score = max(score, 0)
        return score
    def get_category(self, score):
        if score >= 90:
            return "Excellent"
        elif score >= 75:
            return "Good"
        elif score >= 50:
            return "Fair"
        else:
            return "Poor"
        