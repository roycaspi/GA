# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import re

from utils import *
import matplotlib.pyplot as plt
from tqdm import tqdm


def allstars(directory_path, filename, mu, n):
    """
    Creating a base population of strong individuals from a directory of documented
    GA run results, assuming an individual found in a GA run is a route containing
    good (short) sub-routes, thus recombining strong individuals should potentially
    return stronger offspring.
    :param directory_path:  the directory of documented runs.
    :param filename:        the format of a file name.
    :param mu:              size of the population to return.
    :param n:               length of the permutation (route).
    :return: a list of "allstar" individuals.
    """
    runs_n = len(os.listdir(directory_path)) // 2  # each run has log file and plot
    allstars = []
    fit = []
    for run in range(runs_n):
        with open(directory_path + f"{filename}{run}.txt", 'r') as reader:
            lines = reader.readlines()
        fitness = float(lines[11].split()[0])
        if fitness in fit:
            continue            # avoid duplications
        star = []
        for line in lines[2:11]:                     # the route is documented in these lines
            star += [int(x) for x in re.split('\W+', line) if x.isalnum()]
        allstars.append(np.array(star))
        fit.append(fitness)
    while len(allstars) < mu:
        allstars.append(np.random.permutation(n) + 1)
    if len(allstars) > mu:
        Population.roulette_select(allstars, fit, mu)
        # worst = max(fit)
        # allstars.pop(fit.index(worst))
        # fit.remove(worst)
    return allstars


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    f = open("tokyo.dat")
    d = Destinations(f)
    f.close()

    """ configuration parameters """
    n = 150
    max_evals = 10 ** 5
    Nruns = 10
    mu = 200
    pc = 1
    pm = 2 / n
    crossover_implementation = "order"
    lam = 200
    elitism = True
    seed = None
    rand_couple = False  # a heuristic parameter inserting 2 random individuals to each new generation
    rand_elite = 0  # a heuristic parameter determines probability to switch off elitism in an iteration
    allstars_heu = True  # documentation above

    """ log parameters """
    log_dir = os.getcwd() + "\\log\\"
    logfile_name = "run_log"
    plotfile_name = "run_plot"

    """ main logging file - documents global stats """
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

    for run in range(Nruns):

        history = []
        if allstars_heu:
            p = Population(
                [Individual(star, n, d.fitnessFunc, local_state) for star in allstars(log_dir, logfile_name, mu, n)],
                lam, d.fitnessFunc, local_state, elitism
            )
        else:
            p = Population(
                [Individual(np.random.permutation(n) + 1, n, d.fitnessFunc, local_state) for __ in range(mu)],
                lam, d.fitnessFunc, local_state, elitism
            )
        eval_ctr = mu
        curr_f, curr_r = best_f, best_r = p.best()
        history.append(curr_f)

        pbar = tqdm(total=max_evals // lam)
        while eval_ctr < max_evals:

            # recombination (crossover, mutation) -> selection
            p.select_generation(
                p.generate_generation(pm, pc, crossover_dict[crossover_implementation], rand_couple), rand_elite)

            eval_ctr += lam
            curr_f, curr_r = p.best()
            if curr_f < best_f:
                best_f, best_r = curr_f, curr_r
            history.append(curr_f)
            if np.mod(eval_ctr, max_evals // 10) == (mu if mu != lam else 0):
                print(f"{eval_ctr} evals:\n"
                      f"Current best fitness: {best_f} for the route:\n{best_r}\n" + '=' * 60)
            pbar.update()

        plt.semilogy(np.array(history))
        plt.title(f"Run {runs_n}")
        plt.savefig(log_dir + f'{plotfile_name}{runs_n}.png')
        plt.show()
        run_log = os.open(os.getcwd() + "\\log\\" + f'{logfile_name}{runs_n}.txt', os.O_CREAT | os.O_RDWR)
        os.write(run_log, str.encode(f"Run {runs_n}:\n"
                                     f"Shortest route found:\n{best_r}\n"
                                     f"{best_f} km long\n\n{'=' * 60}\n"
                                     f"Run Parameters:\n"
                                     f"n = {n}\nmax_evals = {max_evals}\nNruns = {Nruns}\nmu = {mu}\npc = {pc}\n"
                                     f"pm = {pm}\ncrossover_implementation = {crossover_implementation}\nlam = {lam}\n"
                                     f"elitism = {elitism}\nseed = {seed}\nrand_couple = {rand_couple}\n"
                                     f"rand_elite = {rand_elite}\nallstars_heu = {allstars_heu}"))
        print(f"{eval_ctr} evals:\n"
              f"Current best fitness: {best_f} for the route:\n{best_r}\n" + '=' * 60)

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
        pbar.close()

    print('\n' + '=' * 60)
    print(f"Best ever: {best_result} achieved in run num: {best_run}\n")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
