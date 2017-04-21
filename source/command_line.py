
import sys
import argparse

import source.gaston as gaston_alg

DESCRIPTION = 'A command line interface for interacting with the gaston python implementation.'

def main():
    """
    A command line interface for interacting with the gaston python implementation.
    Args:
        min_support: a float or integer
        input_file: file path to a text file in line graph format
        output_file: file path to output frequent subgraphs in line graph format
        dont_generate_cycles: a flag to specify that cycles should not be generated
        don_generate_trees: a flag to specify that trees should not be generated

    Example: python main.py -s 0.95 -i test_files/medium_chemical.txt -o output_files/output.txt -c -t
    """

    # Parse command line input
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument("min_support", type=float, help='Minimum support for the gaston algorithm.')
    parser.add_argument("input_file",
                        help='Input file path containing graphs in line graph format.')
    parser.add_argument("-o", "--output_file", help='Ouput file path.')
    parser.add_argument("-c", "--dont_generate_cycles", default=False,
                        help='Do not generate cyclic subgraphs.', action="store_true")
    parser.add_argument("-t", "--dont_generate_trees", default=False,
                        help='Do not generate tree subgraphs.', action="store_true")

    args = parser.parse_args()

    # Validate input
    if args.min_support <= 0:
        raise argparse.ArgumentTypeError("Minimum support must be greater than 0.")

    print("\nMinimum Support:{}".format(args.min_support))

    if args.dont_generate_cycles:
        print("Cycles will not be generated.")

    if args.dont_generate_trees:
        print("Trees will not be generated.")

    frequent_output = gaston_alg.gaston(args.min_support, args.input_file,
                                        args.dont_generate_cycles, args.dont_generate_trees,
                                        should_print_graph_information=True)

    if args.output_file is not None:
        gaston_alg.write_frequent_subgraphs_to_file_path(args.output_file, frequent_output)

    gaston_alg.print_statistics(frequent_output)
