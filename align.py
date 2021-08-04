#!/usr/bin/env python3


import argparse
from Modules.SW import SmithWaterman
from Modules.ScalabilityTest import OtherAlgorithm

def Other(s1,s2,scores):
    print("""This is just a test""")


# A dictionary containing all the classes that have been imported. Every class represent an alignment algorithm.
# At the moment only the "Smith-Waterman" algorithm is implemented, but "OtherAlgorithm" can be launched to see
# the scalability potential of the program.
algs = {"SmithWaterman":SmithWaterman,"Other":OtherAlgorithm}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""align.py - easily scalable program for sequence alignment""",
    epilog= 'UNITN - Algorithms for Bioinformatics - July 2021 - Paolo Bianco')

    parser.add_argument("algorithm", type = str,
                                        help = "The algorithm you want to use. [Input type: <str>. Accepted param: 'SmithWaterman', 'Other']")

    parser.add_argument("seq1", type = str,
                                        help = "The first sequence you want to align [Input type: <str>]")

    parser.add_argument("seq2", type = str,
                                        help = "The second sequence you want to align [Input type: <str>]")

    parser.add_argument("-s", "--scores", type = int, nargs=3, default=[1,-1,-2],
            help="The scores to be used during the lignment. How to use: '-s 2 -2 -3'.[Input type: <int>. Default values: match=1, mismatch=-1, gap=-2]")

    parser.add_argument("-f", "--filter", type = str, default="best",
            help="Filtering parameters used to retrieve the desired alignments.Accepted parameters: 'best' - get the alignments with the highest score -, 'all' - get all the possible alignment, 'filter' - get the filtered alignment as requested during the exam [Input type: <str>. Default: 'best']")

    parser.add_argument('--no-matrix', dest='printMatrix', action='store_false', help="Add the flag '--no-matrix' if you do not want to print the Scoring Matrix given by the Smith-Waterman algorithm\n(by default the matrix is printed)")
    parser.set_defaults(printMatrix=True)
    
    parser.add_argument('--verbose', dest='verbose', action='store_true', help="Add the flag '--verbose' if you want in depth statistics about the alignment.")
    parser.set_defaults(verbose=False)


    args = parser.parse_args()
    selectedAlgorithm = args.algorithm
    sequence1 = args.seq1
    sequence2 = args.seq2
    scores = args.scores
    printScoringMatrix = args.printMatrix
    filteringParam = args.filter
    verbose = args.verbose
    algs[selectedAlgorithm](sequence1,sequence2,printScoringMatrix,filteringParam,verbose,scores)()    
    


    
