import argparse
import sys
from pathlib import Path

# Add project root to Python's search path
sys.path.append(str(Path(__file__).resolve().parent))

from src.pipeline import DatasetPipeline


def main():

    parser = argparse.ArgumentParser(

        description="Dataset Quality Engine"

    )

    parser.add_argument(

        "--input",

        required=True,

        help="Path to dataset"

    )

    args = parser.parse_args()

    pipeline = DatasetPipeline(

        dataset_path=args.input

    )

    pipeline.run()


if __name__ == "__main__":

    main()
