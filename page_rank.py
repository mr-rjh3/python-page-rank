import argparse
import os.path
import json

def pageRank(nodeDict, maxiterations, arglambda, threshold, iteration=0, currentPageRank={}):
    if(iteration == 0):
        # initialize page rank for each node. We assume that each PR is equal initially
        for node in nodeDict:
            currentPageRank[node] = 1/len(nodeDict)
    if(iteration >= maxiterations):
        return currentPageRank, iteration

    # Begining of Page Rank calculation
    newPageRank = {}
    for node in nodeDict:
        # get the list of nodes that point to this node
        inNodes = nodeDict[node][0]

        # calculate the page rank for this node
        pRank = 0
        for inNode in inNodes: # for each node that links to this node
            numberOfOutNodes = len(nodeDict[inNode][1]) # get the number of outgoing links
            pRank += currentPageRank[inNode]/numberOfOutNodes # add the page rank of the node divided by the number of it's outgoing links
        pRank = (arglambda/len(nodeDict)) + ((1-arglambda)*pRank) # calculate the page rank for this node
        newPageRank[node] = pRank # add the new page rank to the dictionary
    # End of Page Rank calculation
    
    # check if the change in page rank is less than the threshold
    change = 0
    for node in nodeDict:
        change += abs(currentPageRank[node] - newPageRank[node])
    if(change < threshold):
        # return the new page rank and the number of iterations (iteration + 1 because we are returning the number of iterations that have been completed)
        return newPageRank, iteration + 1 
    else: 
        # Otherwise call the function again with the new page rank
        return pageRank(nodeDict, maxiterations, arglambda, threshold, iteration+1, newPageRank)

def readNodesfromFile(filename):
    # Returns a dictionary of tuples with the key being the node number => N : (Nodes that point to N, Nodes that N points to)
    nodeDict = {}
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            for line in f:
                if(line[0] == "#"):
                    continue # skip comments
                source = int(line.split("\t")[0]) # first column is the source ID
                dest = int(line.split("\t")[1]) # second column is the destination ID
                if(source not in nodeDict):
                    # create a new entry in the dictionary
                    nodeDict[source] = ([], []) 
                if(dest not in nodeDict):
                    # create a new entry in the dictionary
                    nodeDict[dest] = ([], []) 
                nodeDict[source][1].append(dest) # add the destination to the list of nodes that the source points to
                nodeDict[dest][0].append(source) # add the source to the list of nodes that are pointing to the destination
    else:
        print("File does not exist")
    return nodeDict

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Page Rank Program')
    parser.add_argument("-i", "--maxiteration", help="Maximum number of iterations the program will complete.", default=3, type=int)
    parser.add_argument("-l", "--arglambda", help="The lambda / random surfer parameter value.", default=0.85, type=float)
    parser.add_argument("-t", "--threshold", help="The threshold value. The program will stop once the total difference in all nodes page rank change is less than this value.", default=0.0001, type=float)
    parser.add_argument("-n", "--nodes", help="The Node IDs that we want to get page rank from. Usage: -n/--nodes node1 node2 node3 ...", default=[], nargs='+', type=int) # nargs='+' means 1 or more
    parser.add_argument("-d", "--dump", help="Dumps page rank to JSON file when True.",action="store_true", default=False)

    args = parser.parse_args()
    # Conditional print statements
    if(len(args.nodes) == 0):
        print("Finding Page Rank with max iterations: ", args.maxiteration, " lambda: ", args.arglambda, " threshold: ", args.threshold)
    else:
        print("Finding Page Rank for nodes: ", args.nodes, " with max iterations: ", args.maxiteration, " lambda: ", args.arglambda, " threshold: ", args.threshold)
    
    # Read nodes from file and store them in a dictionary with the key being the node number => N : (Nodes that point to N, Nodes that N points to)
    nodeDict = readNodesfromFile("web-Stanford.txt")

    # Calculate page rank and store it in a dictionary with the key being the node number => N : Page Rank
    pageRankDict, iteration = pageRank(nodeDict, args.maxiteration, args.arglambda, args.threshold)
    print("Page Rank found after ", iteration, " iterations.")

    # if the user specified nodes to get page rank from, print them out
    if(len(args.nodes) > 0):
        print("Node:\tPage Rank:")
        for node in args.nodes:
            print("{}\t{}".format(node, pageRankDict[node]))

    # if the user specified to dump the page rank to a JSON file, do so
    if(args.dump):
        with open("pageRank.json", 'w') as f:
            json.dump(pageRankDict, f, indent=4)