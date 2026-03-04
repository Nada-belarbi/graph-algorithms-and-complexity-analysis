import random
import time
import matplotlib.pyplot as plt
import copy
import sys

def isSorted(l):
    for i in range(len(l) - 1):
        if l[i] > l[i + 1]: return False
    return True

def areSorted(ll):
    for i in range(len(ll)):
        if not isSorted(ll[i]): return (False, i)
    return (True, 0)

def create_data(nlist=15, nval=200):
    
    # Création de listes de taille incrémentale et de contenu aléatoire
    listDataRandom = []
    listDataSorted = []
    listDataInversedSorted = []
    sizeArrays = []
    
    # Remplissage des listes
    for i in range(1, nlist + 1):
        s = nval * i 
        dataRandom = s*[0]
        dataSorted = s*[0]
        dataInversed = s*[0]
        for j in range(s):
            dataRandom[j]=j
            dataSorted[j]=j
            dataInversed[j]=j
            
        dataInversed.reverse()
        random.shuffle(dataRandom)
        
        listDataRandom.append(dataRandom)
        listDataSorted.append(dataSorted)
        listDataInversedSorted.append(dataInversed)
        sizeArrays.append(s)

    return(sizeArrays, listDataRandom, listDataSorted, listDataInversedSorted)

def executerTri(fct_tri, color, nom, nlist=15, nval=200, surplace = True):
    
    axis, listDataRandom, listDataSorted, listDataInvertedSorted = create_data(nlist, nval)
    
    toplotRandom = []
    toplotSorted = []
    toplotInverted = []
    
    dataTestRandom    = copy.deepcopy(listDataRandom)
    dataTestSorted    = copy.deepcopy(listDataSorted)
    dataTestInverted  = copy.deepcopy(listDataInvertedSorted)
    
    for i in range(len(axis)):
        time1 = time.time()
        if surplace:
            fct_tri(dataTestRandom[i])
        else:
            dataTestRandom[i] = fct_tri(dataTestRandom[i])
        time2 = time.time()
        toplotRandom.append((time2 - time1) * 1000)
        time3 = time.time()
        if surplace:
            fct_tri(dataTestSorted[i])
        else:
            dataTestSorted[i] = fct_tri(dataTestSorted[i])
        time4 = time.time()
        toplotSorted.append((time4 - time3) * 1000)
        time5 = time.time()
        if surplace:
            fct_tri(dataTestInverted[i])
        else:
            dataTestInverted[i] = fct_tri(dataTestInverted[i])
        time6 = time.time()
        toplotInverted.append((time6 - time5) * 1000)

    (ok1, ipb1) = areSorted(dataTestRandom)
    (ok2, ipb2) = areSorted(dataTestSorted)
    (ok3, ipb3) = areSorted(dataTestInverted)
    
    if not ok1:
        print(nom + ' data random incorrect, liste #' + str(ipb1))
    else:
        plt.plot(axis, toplotRandom, '-' + color, label=nom + ' (Cas Moyen)')
    if not ok2:
        print(nom + ' data Sorted incorrect, liste #' + str(ipb2))
    else:
        plt.plot(axis, toplotSorted, '--' + color, label=nom + ' (Meilleur Cas)')

    if not ok3:
        print(nom + ' data Inverted incorrect, liste #' + str(ipb3))
    else:
        plt.plot(axis, toplotInverted, ':' + color, label=nom + ' (Pire Cas)')
    plt.xlabel("Taille du tableau")  # Titre de l'axe x
    plt.ylabel("Temps d'exécution (millisecondes)")  # Titre de l'axe y
    plt.title(f"Performance de l'algorithme de tri \"{nom}\"")  # Titre du graphique
    plt.legend()
    plt.show()

def executerTri_quick_sort(fct_tri, color, nom, nlist=15, nval=200, surplace=True):
    axis, listDataSorted, listDataInvertedSorted, listDataRandom = create_data(nlist, nval)

    toplotRandom = []
    toplotSorted = []
    toplotInverted = []

    dataTestRandom = copy.deepcopy(listDataRandom)
    dataTestSorted = copy.deepcopy(listDataSorted)
    dataTestInverted = copy.deepcopy(listDataInvertedSorted)

    for i in range(len(axis)):
        time1 = time.time()
        if surplace:
            fct_tri(dataTestRandom[i], 0, len(dataTestRandom[i])-1)
        else:
            dataTestRandom[i] = fct_tri(dataTestRandom[i], 0, len(dataTestRandom[i])-1)
        time2 = time.time()
        toplotRandom.append((time2 - time1) * 1000)
        time3 = time.time()
        if surplace:
            fct_tri(dataTestSorted[i], 0, len(dataTestSorted[i])-1)
        else:
            dataTestSorted[i] = fct_tri(dataTestSorted[i], 0, len(dataTestSorted[i])-1)
        time4 = time.time()
        toplotSorted.append((time4 - time3) * 1000)
        time5 = time.time()
        if surplace:
            fct_tri(dataTestInverted[i], 0, len(dataTestInverted[i])-1)
        else:
            dataTestInverted[i] = fct_tri(dataTestInverted[i], 0, len(dataTestInverted[i])-1)
        time6 = time.time()
        toplotInverted.append((time6 - time5) * 1000)

    (ok1, ipb1) = areSorted(dataTestRandom)
    (ok2, ipb2) = areSorted(dataTestSorted)
    (ok3, ipb3) = areSorted(dataTestInverted)

    if not ok1:
        print(nom + ' data random incorrect, liste #' + str(ipb1))
    else:
        plt.plot(axis, toplotRandom, '-' + color, label=nom + ' (Cas Moyen)')
    if not ok2:
        print(nom + ' data Sorted incorrect, liste #' + str(ipb2))
    else:
        plt.plot(axis, toplotSorted, '--' + color, label=nom + ' (Meilleur Cas)')

    if not ok3:
        print(nom + ' data Inverted incorrect, liste #' + str(ipb3))
    else:
        plt.plot(axis, toplotInverted, ':' + color, label=nom + ' (Pire Cas)')
    plt.xlabel("Taille du tableau")  # Titre de l'axe x
    plt.ylabel("Temps d'exécution (millisecondes)")  # Titre de l'axe y
    plt.title(f"Performance de l'algorithme de tri \"{nom}\"")  # Titre du graphique
    plt.legend()
    plt.show()