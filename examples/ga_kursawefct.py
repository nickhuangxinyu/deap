#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.

import array
import logging
import random

from deap import algorithms
from deap import base
from deap import benchmarks
from deap import creator
from deap import tools

creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("attr_float", random.uniform, -5, 5)

# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, 3)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def checkBounds(min, max):
    def decCheckBounds(func):
        def wrapCheckBounds(*args, **kargs):
            offspring = func(*args, **kargs)
            for child in offspring:
                for i in xrange(len(child)):
                    if child[i] > max:
                        child[i] = max
                    elif child[i] < min:
                        child[i] = min
            return offspring
        return wrapCheckBounds
    return decCheckBounds

toolbox.register("evaluate", benchmarks.kursawe)
toolbox.register("mate", tools.cxBlend, alpha=1.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=3, indpb=0.3)
toolbox.register("select", tools.selNSGA2)

toolbox.decorate("mate", checkBounds(-5, 5))
toolbox.decorate("mutate", checkBounds(-5, 5)) 

def main():
    random.seed(64)

    MU, LAMBDA = 50, 100
    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("Avg", tools.mean)
    stats.register("Std", tools.std)
    stats.register("Min", min)
    stats.register("Max", max)
    logger = tools.EvolutionLogger(stats.functions.keys())
    
    algorithms.eaMuPlusLambda(toolbox, pop, mu=MU, lambda_=LAMBDA, 
                              cxpb=0.5, mutpb=0.2, ngen=50, 
                              stats=stats, halloffame=hof, logger=logger)

    return pop, stats, hof

if __name__ == "__main__":
    main()
