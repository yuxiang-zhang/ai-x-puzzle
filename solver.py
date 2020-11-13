import heuristics
import puzzle
import searchstrat

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
                strat.search(game)
                strat.retrieve_solution(game.state)
                strat.reset()

if __name__ == '__main__':
    solve_puzzle_file('puzzles/samplePuzzles.txt')