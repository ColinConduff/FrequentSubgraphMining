
Gaston Graph Mining in Python
This is a python implementation of the gaston graph mining algorithm.

"Gaston finds all frequent subgraphs by using a level-wise approach in which first simple paths are considered, 
then more complex trees and finally the most complex cyclic graphs. It appears that in practice most frequent 
graphs are not actually very complex structures; Gaston uses this quickstart observation to organize the search 
space efficiently. To determine the frequency of graphs, Gaston employs an occurrence list based approach in 
which all occurrences of a small set of graphs are stored in main memory." 
- Siegfried Nijssen (Gaston author)

Software Requirements:
 - python 3.2 or later
 - networkx 1.11

 Installation:
 `cd gaston_py`
 `pip install .`

Command Line Interface:
For usage instructions, use the following command.
`gaston -h`

Example:
`gaston 0.95 test_files/medium_chemical.txt -o output_files/output.txt -c -t`

Run Tests:
`python setup.py test`

License