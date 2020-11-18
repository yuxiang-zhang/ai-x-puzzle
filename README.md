https://github.com/yuxiang-zhang/ai-x-puzzle
# ai-x-puzzle
## Instructions to run the program
1. Create an `out` folder which will contain the output search path files and solution path files. 
2. Put the puzzle input files inside the [puzzles](/puzzles/) directory. 
3. In the main scope inside [solver.py](solver.py) script, change the input of `solve_puzzle_file` function to the input file name. 
4. Run the [solver.py](solver.py) script which will generate the search and solution files, analyze their content, and generate a table containing the compiled stats. The compiled stats table will either be output to the console or exported into a `.csv` file inside the same directory. 

## Description of files
- `out` folder contains all search path files and solution files for 50 random puzzles
- `puzzles` folder contains `.txt`file of random puzzles and sample puzzles. 
