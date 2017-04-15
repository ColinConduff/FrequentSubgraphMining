
import unittest
from tests.test_search import SearchTestCase
from tests.test_factory import FactoryTestCase
from tests.test_embedding import EmbeddingTestCase

import sys
from source.main import gaston, command_line_interface

ORIG_CHEM_DATASET = 'test_files/Chemical_340.txt'
SMALL_DATASET = 'test_files/small_chemical.txt'

OUTPUT_FILEPATH = "output_files/output.txt"

if __name__ == '__main__':
    unittest.main()
    
    # gaston(min_support=10,
    #        input_file=SMALL_DATASET,
    #        output_file=OUTPUT_FILEPATH)
    
    # command_line_interface(sys.argv[1:])
