"""Console script for sked_parser."""
import argparse
import sys

from sked_parser import sked_parser


def main():
    """Console script for sked_parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into "
          "sked_parser.cli.main")
    sked_parser.main()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
