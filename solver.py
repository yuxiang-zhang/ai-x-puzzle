import puzzle
import searchstrat
import multiprocessing

if __name__ == '__main__':
    game = puzzle.Puzzle8((3, 0, 1, 4, 2, 6, 5, 7))

    strat = searchstrat.UCS()
    strat.setup_loggers(0)

    p = multiprocessing.Process(target=strat.search, args=tuple([game]))
    p.start()
    p.join(5)

    if p.is_alive():
        p.terminate()
        p.join()

        strat.fail()

    strat.reset()
