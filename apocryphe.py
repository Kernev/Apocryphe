from lapierousse import laroussesynset
from tools.misc import *
import pickle
import random
import sys

sys.modules['laroussesynset'] = laroussesynset  # For pickle


class Apocryphe:  # TOUTE RECHERCHE ICI EST LINEAIRE. SI VOUS N ETES PAS CONTENTS DOMMAGE !
    def __init__(self):
        with open('ressources/databases/jesus', 'rb') as f:  # Bdd importat°
            corpus = pickle.load(f)
            pass
        self.dictionary = init_sub_corpus(corpus, 100)  # dict
        self.lockeds = dict()  # set of keys O(1)
        self.weights = init_weights(self.dictionary)  # dict of weights for optimisation
        self.historique = init_history(self.dictionary)
        self.update_weights()
        self.last_locks = []

        # TODO: fera un filtre de convolution d'apprentissage avec ca && transmettre ca à un serveur.

    def key_exist(self, key):
        return self.dictionary.get(key) is not None

    def compute_row(self, key):
        """This method will count the number of successes in a row of the key in the history"""
        values = self.historique[key][::-1]
        i = 0
        for value in values:
            if value is True:
                i += 1
            else:
                break
        return i

    def random_select(self):
        random_key = random_pond(self.weights)
        return random_key, self.dictionary[random_key]

    def lock(self, key):  # TODO: regarder erreur !
        if self.lockeds.get(key) is None:
            return
        self.lockeds[key] = self.dictionary.pop(key)
        self.last_locks += (key, self.lockeds[key])

    def undo_lock(self):
        if len(self.last_locks) is not 0:
            self.dictionary[self.last_lock[-1][0]] = self.last_lock[-1][1]
            del self.last_lock[-1]

    def count_failures_and_successes(self, key):
        success = 0
        n = len(self.historique[key])
        for value in self.historique[key]:
            if value is True:
                success += 1
        failures = n-success
        return failures, success

    def update_weight(self, key):
        self.weights[key] = space_shape(*self.count_failures_and_successes(key), self.compute_row(key))  # TODO: ca

    def update_weights(self):
        for key in self.weights:
            self.update_weight(key)

    def judge(self, key, boolean):
        if boolean:
            self.historique[key].append(True)
        else:
            self.historique[key].append(False)

    def __str__(self):
        return '[NOT_IMPLEMENTED_YET]'


def init_sub_corpus(dict_, broad=100):  # DEGEULASSE !!!
    temporary_list = [[key, dict_[key]] for key in dict_]
    random.shuffle(temporary_list)

    if broad >= len(temporary_list):
        broad = len(temporary_list) - 1

    temporary_list = temporary_list[0:broad]
    return {item[0]: item[1] for item in temporary_list}


def init_history(dict_):
    return {key: [] for key in dict_}


def init_weights(dict_):
    """Create a new dict with dummy values"""
    return {key: 42 for key in dict_}  # 0 but it can be anything


def random_pond(dict_):
    """WORK ! O(n)"""
    n = int(sum(dict_.values()))
    cumulated_sum = 0
    r = random.randint(0, n-1)
    for key, value in dict_.items():
        if cumulated_sum >= r:
            break
        cumulated_sum += value
    return key


if __name__ == '__main__':
    a = Apocryphe()
    print(a.historique)
    print(a.weights)
    key_, truc = a.random_select()
    print(type(truc))
    print(type(key_))
    a.update_weight(key_)
