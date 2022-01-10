# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from utils import *
import matplotlib.pyplot as plt

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    f = open("tokyo.dat")
    d = Destinations(f)

    """ outer configuration parameters """
    local_state = np.random.RandomState(None)
    n = 150
    max_evals = 10 ** 5
    Nruns = 2

    """ inner configuration parameters """
    mu = 100
    pc = 0.37
    pm = 2/n
    lam = 100
    elitism = True

    for run in range(Nruns):
        fbest = []
        xbest = []
        history = []
        p = Population(
            [Individual(np.random.permutation(n) + 1, n, d.fitnessFunc, local_state) for __ in range(mu)],
            lam, d.fitnessFunc, local_state, elitism
        )
        eval_ctr = mu
        curr_best = best = p.best()
        history.append(curr_best[0])
        while eval_ctr < max_evals:
            p.select_generation(p.generate_generation())
            eval_ctr += lam
            curr_best = p.best()
            if curr_best[0] < best[0]:
                best = curr_best
            history.append(curr_best[0])
            if np.mod(eval_ctr, int(max_evals / 10)) == 0:
                print(f"{eval_ctr} evals:\n"
                      f"Current best fitness: {best[0]} for the route:\n{best[1]}")
            # if fmax == max_attainable:
            #     print(eval_cntr, " evals: fmax=", fmax, "; done!")
            break
        # return xmax, fmax, history
        plt.semilogy(np.array(history))
        plt.show()
        print(f"Run {run}:\n"
              f"Shortest route found:\n{best[1]}\n"
              f"{best[0]} km long")
        fbest.append(best[1])
        xbest.append(best[0])
    print("====\n Best ever: ", min(fbest), "x*=", xbest[fbest.index(min(fbest))])
"""
# Generate offspring population (recombination, mutation)
        newGenome = np.empty([n, mu], dtype=int)
#        1. sexual selection + 1-point recombination
        for i in range(int(mu/2)) :
            p1 = selectfct(Genome,fitness,local_state) 
            p2 = selectfct(Genome,fitness,local_state)
            if local_state.uniform() < pc : #recombination
                idx = local_state.randint(n,dtype=int)
                Xnew1 = np.concatenate((p1[:idx],p2[idx:]))
                Xnew2 = np.concatenate((p2[:idx],p1[idx:]))
            else : #no recombination; two parents are copied as are
                Xnew1 = np.copy(p1)
                Xnew2 = np.copy(p2)
#        2. mutation
            mut1_bits = local_state.uniform(size=(n,1)) < pm
            mut2_bits = local_state.uniform(size=(n,1)) < pm
            Xnew1[mut1_bits] = 1-Xnew1[mut1_bits]
            Xnew2[mut2_bits] = 1-Xnew2[mut2_bits]
#            
            newGenome[:,[2*i-1]] = np.copy(Xnew1)
            newGenome[:,[2*i]] = np.copy(Xnew2)
        #The best individual of the parental population is kept
        newGenome[:,[mu-1]] = np.copy(Genome[:,[np.argmax(fitness)]])
        Genome = np.copy(newGenome)
        Phenotype.clear()
        for k in range(mu) :
            Phenotype.append(decodefct(Genome[:,[k]]))
        fitness = fitnessfct(Phenotype)
        eval_cntr += mu
        fcurr_best = np.max(fitness)
        if fmax < fcurr_best :
            fmax = fcurr_best
            xmax = Genome[:,[np.argmax(fitness)]]
        history.append(fcurr_best)
        if np.mod(eval_cntr,int(max_evals/10))==0 :
            print(eval_cntr," evals: fmax=",fmax)
        if fmax == max_attainable :
            print(eval_cntr," evals: fmax=",fmax,"; done!")
            break
    return xmax,fmax,history
"""



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
