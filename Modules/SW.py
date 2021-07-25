import Modules.DataStructures as ds
import math

class SmithWaterman:



    # The main idea behind this whole class is to treat the score table that is normally built in the Smith Waterman algorithm
    # not just as a simple table, but as a graph (implemented as a list of lists of Nodes). Each Node represent a position (i,j)
    # in the table and has a Score value (look at <DataStructures.py>).
    # When a Node gets a score > 0, it is connected to the previous one to form a connected component. Given a score X, 
    # it is possible to retrieve all the possible alignments by running a BFS algorithm that returns all the possible paths from
    # all the starting Nodes with score X to the end of the single components

    # Initialization of the class.
    # ^
    def __init__(self,seq1,seq2,printSM,filteringParam,verbose,scores = [2,2,2]):

        self.s1, self.s2, self.scores = self.correctnessCheck(seq1,seq2,scores)
        self.nodeTable = list()
        self.graph = ds.Graph()
        self.sortedNodesByScore = dict()
        self.allPaths = dict()

        #parameters
        self.printMatrix = printSM
        self.filteringParam = filteringParam
        self.verbose = verbose



    # This function is called inside <__init__> and controls that the input that is 
    # passed to the class respects the correct format that is needed
    # ^
    def correctnessCheck(self,seq1,seq2,scores):
        
        if seq1.isalpha() == False or seq2.isalpha() == False:
            raise TypeError("Sequences must be of type <string> and characters must be alphabetic only")
       
        if type(scores) != list or len(scores) != 3:
            raise TypeError("Scores must be inserted in the list form [match, mismatch, gap]")


        return seq1.upper(), seq2.upper(), scores
    


    # This function is the first one to be called inside <__call__>. 
    # This function fills <self.nodeTable> with <Node> objects from the DataStructures module.
    # The Nodes are not yet connected into a graph and they are initialized with a 'score' value of 0.
    #
    #   ___________________
    #   |        |        |
    #   |Node_0_0|Node_0_1|
    #   | Score=0| Score=0|
    #   ___________________
    #   |        |        |
    #   |Node_1_0|Node_1_1|
    #   | Score=0| Score=0|
    #   ___________________
    #
    # ^
    def populateNodeTable(self):

        for i in range(len(self.s2) + 1):
            self.nodeTable.append([ds.Node(i,x) for x in range(len(self.s1) + 1)])



    # This function is the second one to be called inside <__call__>.
    # This function has three main objective:
    #
    #        1) for each Node of the <self.nodeTable> that was generated before, compute the Score 
    #           value using the Smit-Waterman procedure.
    #
    #        2) during the computation of the Scores, save in a dictionary <self.sortedNodesByScore> all the Scores
    #           as keys, and lists of Nodes with the corresponding Score as values.  
    #
    #            self.sortedNodesByScore = {1: [node_1_1, node_1_2, ...], 2: [node_1_3, node_1_4, ...], 3: ...}
    #                                       ^            ^
    #                                       |            |
    #                                    score    list of nodes that have that score
    #
    #           This is used in order to easily access the starting points for the alignments based on the scores we
    #           are interested in. 
    #  
    #        3) build a graph with many components, where each connected component corresponds to a sequence alignment.
    # ^
    def fillNodeTable(self):

        """part 1 - table filling"""
        
        n = len(self.s1) + 1
        m = len(self.s2) + 1

        for i in range(1,m):
            for j in range(1,n):
                
                diagonal = -1

                if self.s1[j-1] == self.s2[i-1]:
                    
                    #if match

                    diagonal = self.nodeTable[i-1][j-1].getScore() + self.scores[0]
                else:

                    #if mismatch

                    diagonal = self.nodeTable[i-1][j-1].getScore() + self.scores[1]
                    
                up = self.nodeTable[i-1][j].getScore() + self.scores[2]
                left = self.nodeTable[i][j-1].getScore() + self.scores[2]
                
                choice = max(diagonal,up,left)

                currentNode = self.nodeTable[i][j]
                if choice > 0:                    
                    currentNode.setScore(choice)

                """
                part 2 - self.sortedNodesByScore

                Add each node in the dictionary based on its score 
                """
                
                if choice > 0:
                    if choice not in self.sortedNodesByScore:
                        self.sortedNodesByScore[choice] = [currentNode]
                    else:
                        self.sortedNodesByScore[choice].append(currentNode)

                """part 3 - graph generation"""                    


                if choice == diagonal and currentNode.getScore() > 0:
                    previousNode = self.nodeTable[i-1][j-1]
                    
                    self.graph.insertEdge(currentNode,previousNode)


                if choice == up and currentNode.getScore() > 0:
                    previousNode = self.nodeTable[i-1][j]
                    
                    self.graph.insertEdge(currentNode,previousNode)


                if choice == left and currentNode.getScore() > 0:
                    previousNode = self.nodeTable[i][j-1]
                    
                    self.graph.insertEdge(currentNode,previousNode)
        
        #print("sorted:",self.sortedNodesByScore)
    


    # This function is the third to be called inside <__call__>.
    # This function is responsible for the filtering step: it calls the function <self.generateAlignments()>
    # in oredr to build a dictionary containing all the possible alignments, then it prints only the desired ones
    # depending on the parameters specified as input
    # ^ 
    def filterAlignments(self):

        if self.printMatrix:
            #print the Score matrix
            self.printTable()

        self.generateAlignments()

        print("\n\n\n=============================================")
        print("____ _    _ ____ _  _ _  _ ____ _  _ ___ ____\n|__| |    | | __ |\ | |\/| |___ |\ |  |  [__\n|  | |___ | |__] | \| |  | |___ | \|  |  ___]\n")

        if self.filteringParam == "best":
            tmp_scores = list(self.sortedNodesByScore.keys())
            tmp_scores.sort()
            

            self.printAlignments(tmp_scores[-1])
        elif self.filteringParam == "all":
            tmp_scores = list(self.sortedNodesByScore.keys())
            tmp_scores.sort()
            
            for i in range(len(tmp_scores)-1, -1, -1):
                self.printAlignments(tmp_scores[i])



    # This function is called inside <self.filterAlignments>.
    # For every connected components in the Graph, it runs a BFS algorithm to return all the possible 
    # paths, where each one of them correponds to a possible alignment. The list of Nodes that constitute 
    # a path is then given as input to <self.buildAlignmentString> that converts it into a human-readable form.  
    # ^
    def generateAlignments(self, verbose = False):

        for key in self.sortedNodesByScore:
            for stratingNode in self.sortedNodesByScore[key]:
                paths = self.graph.BFS(stratingNode)
                for path in paths:
                    alignmentTuple = self.buildAlignmentString(path)
                    if key not in self.allPaths:
                        self.allPaths[key] = [alignmentTuple]
                    else:
                        self.allPaths[key].append(alignmentTuple)



    # This function is called inside <self.generateAlignments>.
    # It takes a list of nodes as input (that represent a path) and returns the human-readable alignment
    #
    # from:     path 1 = [node_3_4, node_2_3, node_2_2, node_1_1]
    #
    # to:       GTAC
    #           ** *
    #           GT_C
    # ^
    def buildAlignmentString(self, path, verbose = False):

        seq1_out = ""
        symbols = ""
        seq2_out = ""

        pre_i = int(path[-1].getName().split("_")[1])
        pre_j = int(path[-1].getName().split("_")[2])
        previousIndexes = (pre_i,pre_j)
        
        for k in range(len(path)-2,-1,-1):
            i = int(path[k].getName().split("_")[1])
            j = int(path[k].getName().split("_")[2])

            character1 = "_"
            character2 = "_"
            tmp_symbol = " "

            if i > previousIndexes[0] and j > previousIndexes [1]:
                #match or mismatch
                character1 = self.s1[j - 1]
                character2 = self.s2[i - 1]
                if self.s1[j - 1] == self.s2[i - 1]:
                    #match
                    tmp_symbol = "*"
                else:
                    #mismatch
                    tmp_symbol = "|"
            elif i > previousIndexes[0] and j == previousIndexes[1]:
                #gap on sequence 1
                character2 = self.s2[i - 1]
            elif i == previousIndexes[0] and j > previousIndexes[1]:
                #gap on sequence 2
                character1 = self.s1[j - 1]
            
            seq1_out += character1 
            symbols += tmp_symbol 
            seq2_out += character2 

            previousIndexes = (i,j)

        return (seq1_out, symbols, seq2_out)


    
    # This function prints the Score matrix using ASCII characters
    # ^
    def printTable(self):
        patternLine1 = "_________"
        patternLine2_4 = "|        "
        patternLine3 = ""
        header_line1 = ""
        header_line2 = ""
        header_line3 = ""
        header_line4 = ""

        print("\n============================================================")
        print("____ ____ ____ ____ _ _  _ ____    _  _ ____ ___ ____ _ _  _\n[__  |    |  | |__/ | |\ | | __    |\/| |__|  |  |__/ |  \/\n___] |___ |__| |  \ | | \| |__]    |  | |  |  |  |  \ | _/\_")
        print("\n============================================================")

        # this first for loops prints the first row of the matrix 
        for w in range(len(self.nodeTable[0]) + 1):
            if w == 0 or w == 1:
                #print empty box
                header_line1 += patternLine1
                header_line2 += patternLine2_4
                header_line3 += patternLine2_4
                header_line4 += patternLine2_4
            else:
                tmp_chr = self.s1[w-2]
                patternLine3 = "|    {}   ".format(tmp_chr)

                header_line1 += patternLine1
                header_line2 += patternLine2_4
                header_line3 += patternLine3
                header_line4 += patternLine2_4

        print(header_line1 + "_")
        print(header_line2 + "|")
        print(header_line3 + "|")
        print(header_line4 + "|")

        #this second for loop prints the matrix from row 2 to the end
        for k in range(len(self.nodeTable)):
            tmp_line1 = ""
            tmp_line2 = ""
            tmp_line3 = ""
            tmp_line4 = ""
            
            #print the first column of the matrix 
            #containing the row names
            if k == 0:
                #print empty box
                tmp_line1 += patternLine1
                tmp_line2 += patternLine2_4
                tmp_line3 += patternLine2_4
                tmp_line4 += patternLine2_4
            else:
                tmp_chr = self.s2[k-1]

                patternLine3 = "|    {}   ".format(tmp_chr)

                tmp_line1 += patternLine1
                tmp_line2 += patternLine2_4
                tmp_line3 += patternLine3
                tmp_line4 += patternLine2_4

            #print the rest of the matrix

            for n in self.nodeTable[k]:

                score = n.getScore()
                #print(score)
                lenDigits = len(str(score))
                writingPosition = math.ceil((9-(lenDigits - 1))/2)
                formattedScore = "|"
                for i in range(writingPosition-1):
                    formattedScore += " "
                formattedScore += str(score)
                for i in range(9-(writingPosition + lenDigits)):
                    formattedScore += " "
                
                #print(formattedScore)

                patternLine3 = formattedScore
                #print(patternLine3)

                tmp_line1 += patternLine1
                tmp_line2 += patternLine2_4
                tmp_line3 += patternLine3
                tmp_line4 += patternLine2_4
            
            print(tmp_line1 + "_")
            print(tmp_line2 + "|")
            print(tmp_line3 + "|")
            print(tmp_line4 + "|")
        print(tmp_line1 + "_")



    # This function is called inside <self.filterAlignments> and it prints 
    # the desired alignments
    # ^
    def printAlignments(self,index):

        listAlignment = self.allPaths[index]
        print("===================SCORE {}===================".format(index))
        print("\n---------------------------------------------\n")

        for tupleAlignment in listAlignment:
            print("\tSEQUENCE 1: {}".format(tupleAlignment[0]))
            print("\t            {}".format(tupleAlignment[1]))
            print("\tSEQUENCE 2: {}".format(tupleAlignment[2]))
            if self.verbose:
                print("\n\tAdditional informations:\n")
                n_match = tupleAlignment[1].count("*")
                n_mismatch = tupleAlignment[1].count("|")
                n_gap = tupleAlignment[1].count(" ")
                alignment_lenght = len(tupleAlignment[1])
                print("\t      number of matches: {}".format(n_match))
                print("\t   number of mismatches: {}".format(n_mismatch))
                print("\t         number of gaps: {}".format(n_gap))
                print("\t       alignment lenght: {}".format(alignment_lenght))
                #print("\t percentage of identity")
                #print("\t   of the two sequences")
                #print("\t   given this alignment: {:.3f}".format(n_match/min(len(self.s1),len(self.s2))))
            print("\n---------------------------------------------\n")

            



    # This function is directly called from seqAl.py as a result of the input given to argparse
    # ^  
    def __call__(self):
        self.populateNodeTable()
        self.fillNodeTable()
        self.filterAlignments()
        

if __name__ == "__main__":
    s1 = "TACGGGCC"
    s2 = "TAGCCCT"

    SW = SmithWaterman(s1,s2,[2,-1,-1])()
