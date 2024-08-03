# Librerias
import argparse

# Dataclases

# Funciones

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="feature_extraction",
        description="This script ...",
    )

    parser.add_argument("-we", "--weights", help="Model weights to be loaded", default="")
    parser.add_argument("-w", "--window", help="Window size", default=300)
    parser.add_argument("-t", "--threshold", help="Drowsy detection threshold", default=0.3)
    parser.add_argument("-set", "--simple-ear-threshold", help="Simple EAR threshold", default=0.3)
    parser.add_argument("-o", "--output", help="Output file where features would be saved", default="")
    parser.add_argument("--plot", help="If true plot the feature graphics", action=argparse.BooleanOptionalAction,
        type=bool,
        default=False,
    )

    args = parser.parse_args()