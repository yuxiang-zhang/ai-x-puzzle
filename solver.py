import heuristics
import puzzle
import searchstrat
import multiprocessing
import numpy as np

def solve_puzzle_file(file):
    strats = [
        searchstrat.UCS(),
        searchstrat.GBFS(heuristics.H1()),
        searchstrat.GBFS(heuristics.H2()),
        searchstrat.AStar(heuristics.H1()),
        searchstrat.AStar(heuristics.H2())
    ]
    with open(file, 'r') as f:
        for i, config_str in enumerate(f.readlines()):
            for strat in strats:
                init_config = tuple(map(int, config_str.split(' ')))
                game = puzzle.Puzzle8(init_config)
                strat.setup_loggers(i)
                p = multiprocessing.Process(target=strat.search, args=tuple([game]))
                if has_process_timeout(p, 60):
                    strat.fail()
                strat.reset()

def has_process_timeout(process: multiprocessing.Process, timer: int):
    process.start()
    process.join(timer)

    if process.is_alive():
        process.terminate()
        process.join()
        return True

    return False

def gen_random_puzzle(count=50, x=8):
    X = np.repeat(np.arange(x).reshape(1,-1), count, axis=0)
    return np.array(list(map(np.random.permutation, X)))

if __name__ == '__main__':
    # np.savetxt('puzzles/randomPuzzles.txt', gen_random_puzzle(), fmt='%u')
    # solve_puzzle_file('puzzles/randomPuzzles.txt')
    # solve_puzzle_file('puzzles/samplePuzzles.txt')
    solve_puzzle_file('puzzles/inputPuzzles.txt')
