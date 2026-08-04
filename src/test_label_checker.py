from label_checker import LabelChecker

checker = LabelChecker("dataset")

result = checker.find_missing_labels()

print("=" * 40)
print("MISSING LABEL REPORT")
print("=" * 40)

if result["status"] == "Skipped":

    print(result["reason"])

elif len(result["missing_labels"]) == 0:

    print("No missing labels found.")

else:

    for image in result["missing_labels"]:

        print(image)

print("=" * 40)