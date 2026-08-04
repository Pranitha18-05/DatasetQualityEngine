from bounding_box_validator import BoundingBoxValidator

validator = BoundingBoxValidator(

    "dataset",

    num_classes=3

)

result = validator.validate()

print("=" * 40)

print("BOUNDING BOX REPORT")

print("=" * 40)

if result["status"] == "Skipped":

    print(result["reason"])

elif len(result["errors"]) == 0:

    print("All annotations are valid.")

else:

    for error in result["errors"]:

        print(error)

print("=" * 40)