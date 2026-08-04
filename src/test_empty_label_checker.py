from empty_label_checker import EmptyLabelChecker

checker = EmptyLabelChecker("dataset")

result = checker.find_empty_labels()

print("=" * 40)
print("EMPTY LABEL REPORT")
print("=" * 40)

if result["status"] == "Skipped":

    print(result["reason"])

elif len(result["empty_labels"]) == 0:

    print("No empty label files found.")

else:

    for label in result["empty_labels"]:

        print(label)

print("=" * 40)