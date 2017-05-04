
Gaston Graph Mining with Python
This is a python implementation of the Gaston graph mining algorithm.

"Gaston finds all frequent subgraphs by using a level-wise approach in which first simple paths are considered, 
then more complex trees and finally the most complex cyclic graphs. It appears that in practice most frequent 
graphs are not actually very complex structures; Gaston uses this quickstart observation to organize the search 
space efficiently. To determine the frequency of graphs, Gaston employs an occurrence list based approach in 
which all occurrences of a small set of graphs are stored in main memory." 
- Siegfried Nijssen (Gaston author)

Software Requirements:
 - python 3.2 or later
 - networkx 1.11
 - matplotlib

 Installation:
 `cd gaston_py`
 `pip3 install .`

Command Line Interface:
For usage instructions, use the following command.
`gaston -h`

Examples:
`gaston 0.95 test_files/medium_chemical.txt -o output_files/ -c -t`
`gaston 6 test_files/medium_chemical.txt`
`gaston 2 test_files/Chemical_340.txt`

Notes: 
 - Support is defined as frequency(subgraph) / count(graphs). See reference [1] below for details.
 - If an output directory is provided: 
     * Frequent subgraphs are drawn using matplotlib and saved under [output folder]/graphs/.
     * A `line_graph.txt` file is generated containing the frequent subgraphs in Line Graph format.
 - Test files are available in the `test_files` directory.  The Chemical_340 dataset was obtained 
     from Nijssen and Kok's website.

Run Tests:
`python setup.py test`

Performance:
 - This Python implementation is significantly slower than the original implementation 
      in C++ by Nijssen and Kok, as well as the Java implementation by the ParSeMis library.
 - It is also much slower than gSpan impelementations in Python.  This is likely due
      to the use of an occurrence list, which tracks all subgraphs that have been seen to 
      ensure the correctness of the algorithm.

References:
[1] Siegfried Nijssen and Joost Kok. A Quickstart in Frequent Structure Mining Can 
  Make a Difference. Proceedings of the SIGKDD, 2004.
http://liacs.leidenuniv.nl/~nijssensgr/gaston/index.html

Additional Resources:
Java implementation of the Gaston algorithm
https://www2.cs.fau.de/EN/research/zold/ParSeMiS/index.html
https://github.com/timtadh/parsemis