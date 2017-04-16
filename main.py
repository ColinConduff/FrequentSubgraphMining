
import unittest
from tests.test_search import SearchTestCase
from tests.test_factory import FactoryTestCase
from tests.test_embedding import EmbeddingTestCase

import sys
from source.main import gaston, print_statistics, command_line_interface

ORIG_CHEM_DATASET = 'test_files/Chemical_340.txt'
SMALL_DATASET = 'test_files/small_chemical.txt'
MEDIUM_DATASET = 'test_files/medium_chemical.txt'

OUTPUT_FILEPATH = "output_files/output.txt"

if __name__ == '__main__':
    unittest.main()
    
    # frequent_output = gaston(min_support=0.95,
    #                          input_file=MEDIUM_DATASET,
    #                          dont_generate_trees=True,
    #                          dont_generate_cycles=True)

    # write_to_file(OUTPUT_FILEPATH, frequent_output)
    # print_statistics(frequent_output)
    
    #python3 main.py -s 0.95 -i test_files/medium_chemical.txt -o output_files/output.txt -c -t
    # command_line_interface(sys.argv[1:])
