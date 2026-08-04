import pandas as pd
import matplotlib.pyplot as plt

class DatasetStatistics:

    def __init__(self):
        self.records = []
    def add_record(self,filename,blur_score,blur_status,brightness,brightness_status,width,height,resolution_status,quality_score,quality_category):
        self.records.append({

    "Filename": filename,

    "Blur Score": blur_score,

    "Blur Status": blur_status,

    "Brightness": brightness,

    "Brightness Status": brightness_status,

    "Width": width,

    "Height": height,

    "Resolution Status": resolution_status,

    "Quality Score": quality_score,

    "Quality Category": quality_category

    })
    def to_dataframe(self):
        return pd.DataFrame(self.records)
    def save_report(self, filename="reports/dataset_statistics.csv"):
        if not self.records:
            print("Warning: No records to save.")
            return
        df = self.to_dataframe()
        df.to_csv(filename, index=False)
    def print_summary(self):
        if not self.records:
            print("No records available.")
            return
        df = self.to_dataframe()
        total_images = len(df)
        blurry_images = len(df[df["Blur Status"] == "Blurry"])
        dark_images = len(df[df["Brightness Status"] == "Too Dark"])
        bright_images = len(df[df["Brightness Status"] == "Too Bright"])
        small_images = len(df[df["Resolution Status"] == "Too Small"])
        average_blur = df["Blur Score"].mean()
        average_brightness = df["Brightness"].mean()
        average_width = df["Width"].mean()
        average_height = df["Height"].mean()
        print("\n===== DATASET SUMMARY =====")
        print(f"Total Images      : {total_images}")
        print(f"Blurry Images     : {blurry_images}")
        print(f"Too Dark Images   : {dark_images}")
        print(f"Too Bright Images : {bright_images}")
        print(f"Too Small Images  : {small_images}")
        print(f"Average Blur      : {average_blur:.2f}")
        print(f"Average Brightness: {average_brightness:.2f}")
        print(f"Average Resolution: {average_width:.0f} x {average_height:.0f}")
        scores = [record["Quality Score"]for record in self.records]
        average_score = sum(scores) / len(scores)
        print(f"Average Quality Score : {average_score:.2f}")
        excellent = 0
        good = 0
        fair = 0
        poor = 0
        for record in self.records:

            category = record["Quality Category"]

            if category == "Excellent":

                excellent += 1

            elif category == "Good":

                good += 1

            elif category == "Fair":

                fair += 1

            else:

                poor += 1
        print(f"Excellent Images : {excellent}")

        print(f"Good Images      : {good}")

        print(f"Fair Images      : {fair}")

        print(f"Poor Images      : {poor}")
        dataset_quality = average_score
        print(f"Dataset Quality : {dataset_quality:.2f}%")
    def save_quality_report(self):
        quality_records = []
        for record in self.records:
            quality_records.append({

    "Filename": record["Filename"],

    "Blur Status": record["Blur Status"],

    "Brightness Status": record["Brightness Status"],

    "Resolution Status": record["Resolution Status"],

    "Quality Score": record["Quality Score"],

    "Quality Category": record["Quality Category"]

})
        df = pd.DataFrame(quality_records)
        df.to_csv(

    "reports/quality_report.csv",

    index=False

)
    def plot_quality_distribution(self):
        excellent = 0
        good = 0
        fair = 0
        poor = 0
        for record in self.records:
            category = record["Quality Category"]
            if category == "Excellent":
                excellent += 1
            elif category == "Good":
                good += 1
            elif category == "Fair":
                fair += 1
            else:
                poor += 1
        categories = ["Excellent","Good","Fair","Poor"]
        counts = [excellent,good,fair,poor]
        plt.figure(figsize=(8,5))
        plt.bar(categories,counts)
        plt.title("Quality Category Distribution")
        plt.xlabel("Quality Category")
        plt.ylabel("Number of Images")
        plt.savefig("reports/quality_distribution.png")
        plt.close()