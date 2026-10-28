"""Variable-length chromosomes: passes may be omitted or repeated."""
import random
from passes import PASS_NAMES
MIN_LEN,MAX_LEN=1,12

def random_sequence(): return [random.randrange(len(PASS_NAMES)) for _ in range(random.randint(MIN_LEN,MAX_LEN))]
def initial_population(size): return [random_sequence() for _ in range(size)]
def crossover(a,b):
    child=list(a[:random.randint(0,len(a))])+list(b[random.randint(0,len(b)):])
    return (child or [random.randrange(len(PASS_NAMES))])[:MAX_LEN]
def mutate(sequence,rate=.2):
    child=list(sequence)
    if random.random()>=rate: return child
    op=random.choice(['replace','swap','insert','delete'])
    if op=='replace': child[random.randrange(len(child))]=random.randrange(len(PASS_NAMES))
    elif op=='swap' and len(child)>1:
        i,j=random.sample(range(len(child)),2); child[i],child[j]=child[j],child[i]
    elif op=='insert' and len(child)<MAX_LEN: child.insert(random.randrange(len(child)+1),random.randrange(len(PASS_NAMES)))
    elif op=='delete' and len(child)>MIN_LEN: del child[random.randrange(len(child))]
    return child
