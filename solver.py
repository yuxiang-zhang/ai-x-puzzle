import puzzle
import heuristics
import searchstrat
import multiprocessing
import numpy as np
import pandas as pd

def solve_puzzle_file(file, strats, goals=None, shape=None, countdown=60):
    with open(file, 'r') as f:
        for i, config_str in enumerate(f.readlines()):
            for strat in strats:
                init_config = tuple(map(int, config_str.split(' ')))
                if goals is None:
                    game = puzzle.Puzzle(init_config, puzzle.OldPuzzle.goals, (2, 4))
                else:
                    game = puzzle.Puzzle(init_config, goals, shape)
                strat.setup_loggers(i)
                p = multiprocessing.Process(target=strat.search, args=tuple([game]))
                if has_process_timeout(p, countdown):
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

def compile_stats(strats, count=50, dir_path ='out/'):
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
        file_path = '{:s}{:s}_{:s}_{:s}.txt'.format(dir_path, '{:d}', str(algo), '{:s}')
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
    x3x3_goal = [tuple(range(9)), tuple((1,2,3,4,5,6,7,8,0))]
    x4x4_goal = [tuple(range(16)), tuple(list(range(1,16))+[0])]

    countdown = 5

    # Control which Algorithms to use:
    all_strats = (
        # searchstrat.UCS(heuristics.H0(puzzle.OldPuzzle.goals)),
        # searchstrat.GBFS(heuristics.H1(puzzle.OldPuzzle.goals)),
        # searchstrat.GBFS(heuristics.H2(puzzle.OldPuzzle.goals)),
        # searchstrat.GBFS(heuristics.H3(puzzle.OldPuzzle.goals)),
        # searchstrat.GBFS(heuristics.H4(puzzle.OldPuzzle.goals)),
        # searchstrat.GBFS(heuristics.H5(puzzle.OldPuzzle.goals)),
        # searchstrat.AStar(heuristics.H0(puzzle.OldPuzzle.goals)),
        # searchstrat.AStar(heuristics.H1(puzzle.OldPuzzle.goals)),
        # searchstrat.AStar(heuristics.H2(puzzle.OldPuzzle.goals)),
        # searchstrat.AStar(heuristics.H3(puzzle.OldPuzzle.goals)),
        # searchstrat.AStar(heuristics.H4(puzzle.OldPuzzle.goals)),
        # searchstrat.AStar(heuristics.H5(puzzle.OldPuzzle.goals)),
        # searchstrat.AStar(heuristics.H1(x3x3_goal)),
        # searchstrat.AStar(heuristics.H2(x3x3_goal)),
        # searchstrat.AStar(heuristics.H1(x4x4_goal)),
        # searchstrat.AStar(heuristics.H2(x4x4_goal)),
    )

    # Generate random puzzles:
    # np.savetxt('puzzles/3x3.txt', X=gen_random_puzzle(x=3*3), fmt='%u')
    # np.savetxt('puzzles/4x4.txt', X=gen_random_puzzle(count=3, x=4*4), fmt='%u')

    # Generate puzzles:
    # solve_puzzle_file('puzzles/3x3.txt', all_strats, goals=x3x3_goal, shape=(3,3), countdown=100)
    # solve_puzzle_file('puzzles/4x4.txt', all_strats, goals=x4x4_goal, shape=(4,4), countdown=100)
    solve_puzzle_file('puzzles/randomPuzzles.txt', all_strats)
    # solve_puzzle_file('puzzles/samplePuzzles.txt', all_strats)
    # solve_puzzle_file('puzzles/inputPuzzles.txt', all_strats)

    # Compile statistics:
    print(compile_stats(all_strats, count=50).T)
