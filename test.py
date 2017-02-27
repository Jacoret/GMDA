# Où l'on mesure le diamètre de feuilles.

from testFunctions import createTD1, createTD2, testTree
from kdtree import create
import numpy as np
import pandas as pd
import logging
logging.basicConfig(filename='test_log.txt', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- Variables à itérer ---
D = [2, 5, 10, 20]
Jit = [0, 1, 3]

results = pd.DataFrame(columns=['test_id', 'n', 'd', 'jit_coef',
                                'picked_depth', 'halving_depth'])

compt = 1
for iteration in range(10):
    for test_id in [1, 2]:
        for d in D:
            n = 100 * d
            if test_id == 1:
                data = createTD1(n, d)
            elif test_id == 2:
                data = createTD2(n, d, np.floor(d/2))

            for j, jit in enumerate(Jit):
                print("DS of type %i, dim (%i,%i) and jit coeff %.2f... "
                      % (test_id, data.shape[0], data.shape[1], jit), end="")
                testresults = testTree(data, cs=10, md=10, jit=jit)
                test_info = np.append(np.append(test_id, data.shape), jit)
                results.loc[compt] = np.append(test_info, testresults)
                compt += 1
                print("done.\n")

# Doubling dimension
results.loc[results.test_id == 1,
            'dd'] = np.log(results.loc[results.test_id == 1, 'n'])

results.loc[results.test_id == 2,
            'dd'] = np.floor(d/2) * np.log(results.loc[results.test_id == 2,
                                                       'n'])

# Constantes
results['c0'] = results.dd * np.log(results.dd) / results.n
results['c2'] = results.halving_depth / results.dd*np.log(results.dd)

# Export
results[['test_id', 'n',
         'd', 'picked_depth']] = results[['test_id', 'n',
                                          'd', 'picked_depth']].astype(int)
results.to_csv('results.csv')

results.head(20)
