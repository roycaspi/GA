# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os

from utils import *
import matplotlib.pyplot as plt
from tqdm import tqdm

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    f = open("tokyo.dat")
    d = Destinations(f)
    f.close()

    """ configuration parameters """
    n = 150
    max_evals = 10 ** 5
    Nruns = 1
    mu = 100
    pc = 0.37
    pm = 2/n
    crossover_implementation = "mapped"
    lam = 100
    elitism = True
    seed = None

    """ main logging file - document all runs """
    with open('logger.txt') as reader:
        lines = reader.readlines()
    runs_n = int(lines[0].split()[-1])
    tf_cals = int(lines[1].split()[-1])
    best_result = float(lines[2].split()[-1])
    best_run = int(lines[3].split()[-1])
    f.close()
    local_state = np.random.RandomState(seed)
    crossover_dict = {
        "mapped": 0,
        "order": 1
    }

    fbest = []
    rbest = []

    for run in tqdm(range(Nruns)):
        print()         # line down after progress bar
        history = []

        p = Population(
            [Individual(np.random.permutation(n) + 1, n, d.fitnessFunc, local_state) for __ in range(mu)],
            lam, d.fitnessFunc, local_state, elitism
        )
        eval_ctr = mu
        curr_f, curr_r = best_f, best_r = p.best()
        history.append(curr_f)

        # recombination (crossover, mutation) -> selection
        p.select_generation(
            p.generate_generation(pm, pc, crossover_dict[crossover_implementation]))

        while eval_ctr < max_evals:
            eval_ctr += lam
            curr_f, curr_r = p.best()
            if curr_f < best_f:
                best_f, best_r = curr_f, curr_r
            history.append(curr_f)
            if np.mod(eval_ctr, int(max_evals / 10)) == 0:
                print(f"{eval_ctr} evals:\n"
                      f"Current best fitness: {best_f} for the route:\n{best_r}\n" + '='*60)

        plt.semilogy(np.array(history))
        plt.title(f"Run {runs_n}")
        plt.savefig(os.getcwd() + "\\log\\" + f'run_plot{runs_n}.png')
        plt.show()
        run_log = os.open(os.getcwd() + "\\log\\" + f'run_log{runs_n}.txt', os.O_CREAT | os.O_RDWR)
        os.write(run_log, str.encode(f"Run {run}:\n"
                                     f"Shortest route found:\n{best_r}\n"
                                     f"{best_f} km long\n\n{'=' * 60}\n"
                                     f"Run Parameters:\n"
                                     f"n = {n}\nmax_evals = {max_evals}\nNruns = {Nruns}\nmu = {mu}\npc = {pc}\n"
                                     f"pm = {pm}\ncrossover_implementation = {crossover_implementation}\nlam = {lam}\n"
                                     f"elitism = {elitism}\nseed = {seed}"))
        fbest.append(best_f)
        rbest.append(best_r)

        tf_cals += eval_ctr
        if best_f < best_result:
            best_result = best_f
            best_run = runs_n
        runs_n += 1

        # write to logger
        log_params = [runs_n, tf_cals, best_result, best_run]
        for i in range(len(log_params)):
            lines[i] = ' '.join((lines[i].split())[:-1] + [str(log_params[i])])
        with open('logger.txt', 'w') as writer:
            writer.write('\n'.join(lines))

    print('\n' + '='*60)
    print(f"Best ever: {best_result} achieved in run num: {best_run}\n")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
