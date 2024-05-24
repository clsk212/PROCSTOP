import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="nombre del programa",
        description="descripcion",
    )

    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="path....",
    )
    parser.add_argument(
        "-f",
        "--function",
        help="function",
        required=True,
    )
    parser.add_argument(
        "--numeric",
        "",
        help="",
        nargs="+",
        type=float,
        default=[0.3],
    )
    parser.add_argument(
        "--bool",
        default=False,
        action=argparse.BooleanOptionalAction,
        help=""
    )

    args, unknown_args = parser.parse_known_args()
    args = parser.parse_args()

    dict_args = vars(args)

    _input = args.input
    _output = args.output

    _bool = False
    if args.argumento_bool:
        _bool = True