import puzzle
import heuristics
import searchstrat
import multiprocessing
import numpy as np
import pandas as pd


all_strats = (
    searchstrat.UCS(),
    searchstrat.GBFS(heuristics.H1()),
    searchstrat.GBFS(heuristics.H2()),
    searchstrat.AStar(heuristics.H1()),
    searchstrat.AStar(heuristics.H2())
)

def solve_puzzle_file(file, strats=all_strats):
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

def compile_stats(dir = 'out/', strats=all_strats, count=50):
    # search_names = ['f(n)', 'g(n)', 'h(n)'] + list(range(8))
    # solution_names = ['token', 'movecost'] + list(range(8))
    compiled_names = ['Avg Search Length', 'Sum Search Length',
                      'Avg Solution Length', 'Sum Solution Length',
                      'Count No Solution',
                      'Avg Cost', 'Sum Cost',
                      'Avg Runtime', 'Sum Runtime']
    compiled_df = pd.DataFrame(columns=compiled_names)
    for algo in strats:
        cost = np.repeat(0, count)
        runtime = np.repeat(60, count).astype(np.float)
        search_path_total = 0
        solution_path_total = 0
        nosol_count = 0
        file_path = '{:s}{:s}_{:s}_{:s}.txt'.format(dir, '{:d}', str(algo), '{:s}')
        for i in range(count):
            search_file_path = file_path.format(i, 'search')
            solution_file_path = file_path.format(i, 'solution')
            nosol = False
            with open(search_file_path) as f:
                if f.read(len('no solution')) == 'no solution':
                    nosol = True
                else:
                    for search_count, _ in enumerate(f):
                        pass
                    search_path_total += search_count

            if nosol:
                nosol_count += 1
            else:
                with open(solution_file_path) as f:
                    for solution_count, _ in enumerate(f):
                        pass
                solution_path_total += solution_count
                last_line = np.loadtxt(solution_file_path, delimiter=' ', skiprows=solution_count, usecols=[0,1])
                cost[i], runtime[i] = last_line

        compiled_df.loc[str(algo)] = (search_path_total / (count - nosol_count), search_path_total,
                                      solution_path_total / (count - nosol_count), solution_path_total,
                                      nosol_count,
                                      cost.sum() / count, cost.sum(),
                                      runtime.sum() / count, runtime.sum()
                                      )
    return compiled_df

if __name__ == '__main__':
    # np.savetxt('puzzles/randomPuzzles.txt', gen_random_puzzle(), fmt='%u')
    # solve_puzzle_file('puzzles/randomPuzzles.txt')
    solve_puzzle_file('puzzles/samplePuzzles.txt')
    # solve_puzzle_file('puzzles/inputPuzzles.txt')
    print(compile_stats(count=3).T)
