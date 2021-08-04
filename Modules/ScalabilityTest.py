class OtherAlgorithm:
    def __init__(self, seq1, seq2, printSM, filteringParam, verbose, scores):
        self.s1 = seq1
        self.s2 = seq2
        self.scores = scores

        #parameters
        self.printMatrix = printSM
        self.filteringParam = filteringParam
        self.verbose = verbose
    
    def __call__(self):
        print("\nThis is a simple example that shows how easily \nthe program can be expanded by adding new classes\nthat represent alignment algorithms.\n")
