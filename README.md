# python-page-rank

## Purpose
Generates the page rank from a dataset and displays the page rank of specified nodes. Also will dump each node's page rank to a JSON file if desired.

## Usage
1. Download and install [python](https://www.python.org/downloads/)
2. Clone the repo.
3. Run `python ./page_rank.py [-OPTIONS]`

## Options
`-i`, `--maxiteration`
  - Maximum number of iterations the program will complete. Default value is 3.
   
`-l`, `--arglambda`
   - The lambda / random surfer parameter value. Default value is 0.85.
    
 `-t`, `--threshold`
   - The threshold value. The program will stop once the total difference in all nodes page rank change is less than this value.
    
 `-n`, `--nodes`
   - The Node IDs that we want to get page rank from, please ensure they are separated by spaces. Usage: `-n/--nodes node1 node2 node3 ...`
   
  `-d`, `--dump`
 - Dumps page rank of all nodes to JSON file "pageRank.json" when True.
