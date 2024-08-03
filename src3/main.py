import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="data_load",
        description="This script calculates the ROC curves of different features extracted from EAR.",
    )

    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Folder containg the raw videos from UTA structured as directly downloaded from Kaggle.",
    )

    