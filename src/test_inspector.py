from inspector import DatasetInspector

inspector = DatasetInspector("dataset")

info = inspector.inspect()

print("=" * 40)
print("DATASET INSPECTION")
print("=" * 40)

print(f"Dataset Type        : {info['dataset_type']}")
print(f"Total Classes       : {info['total_classes']}")

print("Class Names:")

for name in info["class_names"]:

    print(f"  - {name}")

print(f"Total Images        : {info['total_images']}")

print(f"Average Images/Class: {info['average_images']:.2f}")

print()

print("=" * 40)

print("CLASS DISTRIBUTION")

print("=" * 40)

for class_name in info["class_distribution"]:

    count = info["class_distribution"][class_name]

    percentage = info["distribution_percentages"][class_name]

    print(f"{class_name}")

    print(f"Images     : {count}")

    print(f"Percentage : {percentage:.2f}%")

    print("-" * 40)

print(f"Dataset Status : {info['dataset_status']}")

print(f"Annotation Audit    : {info['annotation_audit']}")

print("=" * 40)