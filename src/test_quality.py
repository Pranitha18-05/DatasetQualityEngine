from quality import QualityScorer

scorer = QualityScorer()

score = scorer.calculate_score(

    "Blurry",

    "Too Dark",

    "Low Resolution"

)

category = scorer.get_category(score)

print(f"Score    : {score}")

print(f"Category : {category}")