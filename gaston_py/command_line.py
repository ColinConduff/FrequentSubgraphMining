
import sys
import os
import argparse

import gaston_py.gaston as gaston_alg
import gaston_py.graph as graph_module

DESCRIPTION = 'A command line interface for interacting with the gaston python implementation.'

def main():
    """
    A command line interface for interacting with the gaston python implementation.
    Args:
        min_support: a float or integer
        input_file_path: file path to a text file in line graph format
        output_folder_path: location to output frequent subgraphs in line graph format and drawings
        dont_generate_cycles: a flag to specify that cycles should not be generated
        don_generate_trees: a flag to specify that trees should not be generated

    Examples: 
    gaston 0.95 test_files/medium_chemical.txt -o output_files/ -c -t
    gaston 6 test_files/medium_chemical.txt
    gaston 3 test_files/Chemical_340.txt
    """

    # Parse command line input
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument("min_support", type=float, help='Minimum support for the gaston algorithm.')
    parser.add_argument("input_file_path",
                        help='Input file path containing graphs in line graph format.')
    parser.add_argument("-o", "--output_folder_path", help='Ouput location for frequent subgraphs.')
    parser.add_argument("-c", "--dont_generate_cycles", default=False,
                        help='Do not generate cyclic subgraphs.', action="store_true")
    parser.add_argument("-t", "--dont_generate_trees", default=False,
                        help='Do not generate tree subgraphs.', action="store_true")

    args = parser.parse_args()

    # Validate input
    if args.min_support <= 0:
        raise argparse.ArgumentTypeError("\n\n\t Minimum support must be greater than 0.\n")
    if not os.path.exists(args.input_file_path):
        raise argparse.ArgumentTypeError(
            "\n\n\t The input file path '{}' does not exist.\n".format(args.input_file_path))
    if args.output_folder_path is not None and not os.path.exists(args.output_folder_path):
        raise argparse.ArgumentTypeError(
            "\n\n\t The output folder path '{}' does not exist.\n".format(args.output_folder_path))

    print("\nMinimum Support:{}".format(args.min_support))

    if args.dont_generate_cycles:
        print("Cycles will not be generated.")

    if args.dont_generate_trees:
        print("Trees will not be generated.")

    frequent_output = gaston_alg.gaston(args.min_support, args.input_file_path,
                                        args.dont_generate_cycles, args.dont_generate_trees,
                                        should_print_graph_information=True)

    gaston_alg.print_statistics(frequent_output)

    # If a file path to an output folder is provided,
    # write frequently occurring subgraphs to 'line_graphs.txt' in line graph format.
    # Also, create a graphs folder if necessary, draw graphs, and save them to a 'graphs' folder.
    if args.output_folder_path is not None:
        print("\nProcessing output...")

        output_dirname = os.path.dirname(args.output_folder_path)
        output_file_path = os.path.join(output_dirname, "line_graphs.txt")
        graph_drawings_file_path = os.path.join(os.path.dirname(args.output_folder_path), "graphs", "")

        if not os.path.exists(graph_drawings_file_path):
            os.makedirs(graph_drawings_file_path)

        gaston_alg.write_frequent_subgraphs_to_file_path(output_file_path, frequent_output)
        graph_module.draw_nx_graphs(graph_drawings_file_path, frequent_output)

    print("Completed execution of program.\n")