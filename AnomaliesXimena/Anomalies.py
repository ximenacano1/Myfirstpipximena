#!/usr/bin/env python3

r"""
Myfirstpipximena module
"""

# Librerias
import numpy as np
# import multiprocessing
import itertools
import pandas as pd


def vectors(n):
    """
    Esta funcion genera dos vectores tipo vector-like, con elementos con valores entre -9 y 9.
    Se siguen los procedimientos descritos por Costa, Dobrescu, Bogdan & Fox (2019).

    Entradas:
        n: longitud de los arreglos
    Salidas:
        v, v_: vectores de tipo vector-like (para el caso en el que n es par)
        u, u_: vectores de tipo vector-like (para el caso en el que n es impar)

    """

    # Se crean los vectores para el caso par
    if n % 2 == 0:
        m = int(n / 2 - 1)

        v = []
        l = np.random.randint(-9, 9, m)
        k = np.random.randint(-9, 9, m)

        l_0 = l[0]
        ks = np.append(l_0, [k])

        v = np.concatenate((ks, -ks))

        v_0 = [0, 0]
        v_ = np.concatenate((v_0, l, -l))

        return v, v_

    # Se crean los vectores para el caso impar
    else:
        m = int((n - 3) / 2)

        l = np.random.randint(-9, 9, m)
        k = np.random.randint(-9, 9, m + 1)

        l_0 = np.array([0])
        ks = np.append(l_0, [k])
        u = np.concatenate((ks, -k))

        k_0 = k[0]
        ls = np.append(l, [k_0])
        ls = np.append(ls, [0])
        ls2 = np.append(l, [k_0])
        u_ = np.concatenate((ls, -ls2))

        return u, u_


def set_solutions(x, y):
    """
    Esta funcion genera un vector solución para el problema descrito en Costa, Dobrescu, Bogdan & Fox (2019).
    La solucion arrojada por esta función puede ser de tipo vector-like o quiral.

    Entradas:
        x, y_: dos vectores de tipo vector-like
    Salidas:
        solution, div: el vector solucion; el minimo comun divisor del vector solucion.
    """
    x = np.array(x)
    y = np.array(y)

    z = sum(x * (y**2)) * x - sum((x**2) * y) * y

    div = np.gcd.reduce(z)
    if div != 0:
        solution = z / div
        solution.astype(int)
        return solution, div
    else:
        solution = z
        solution = solution.astype(int)
        div = 1
        return solution, div


def vector_like_comprobation(q):
    """
    Esta funcion comprueba si un arreglo dado es vector like o quiral.

    Entradas:
        q: un vector cualquiera.
    Salidas:
        0: cuando el arreglo es vector-like
        1: cuando el arreglo es quiral.
    """

    q = np.array(q)
    q.astype(int)

    q_max = np.inf

    # Normalize to positive minimum
    if 0 in q:
        q = q[q != 0]
        return 0
    if q.size == 0:
        return 0
    if q[0] < 0:
        q = -q

    if (  # not 0 in z and
        0 not in [sum(p) for p in itertools.permutations(q, 2)]
        and np.abs(q).max() <= q_max  # avoid vector-like and multiple 0's
    ):
        return 1


def quiral_solutions(n, zmax=30, N=5000):
    """
    Esta funcion entrega el total de soluciones quirales para un n determinado.

    Entradas:
        n: longitud de los arreglos
        zmax: valor maximo de los elementos del arreglo solucion
        N: numero de las iteraciones para encontrar todas las soluciones

    Salidas:
        df: data frame que contiene la informacion de l, k, solution, solitionStr y gcd

    Nota: el solutionStr se usa para poder eliminar los valores duplicados de las soluciones
    """

    soluciones = []
    count = 0

    # creamos un dataframe para guardar las soluciones quirales
    df = pd.DataFrame(columns=["l", "k", "solution", "solutionStr", "gcd"])

    for i in range(0, N):

        x, y = vectors(n)
        x = np.array(x)
        y = np.array(y)
        solution, gcd = set_solutions(x, y)
        solution = solution.astype(int)

        # Se aplican las condiciones de la suma y la suma al cubo
        if np.sum(solution) == 0 and np.sum(solution**3) == 0:
            # Se descartan soluciones vector like
            if vector_like_comprobation(solution) == 1:
                p = 0
                for j in solution:
                    # Se dejan las soliciones que cumpla con que sus entradasean menor a 30
                    if j < zmax:
                        p += 1
                # Se descartan las soluciones triviales
                if p == len(solution) and (np.all(solution == 0)) == False:
                    if np.all(abs(solution) < zmax) == True:
                        # Se guarda la solucion en un dataframe de pandas
                        count += 1
                        if n % 2 == 0:
                            solution_sort = np.unique(sorted(solution, key=abs))
                            solution_sort = np.array(solution_sort)
                            StrSol = np.array2string(solution_sort)
                            df = df.append(
                                {
                                    "l": x,
                                    "k": y,
                                    "solution": solution,
                                    "solutionStr": StrSol,
                                    "gcd": gcd,
                                },
                                ignore_index=True,
                            )

                        else:
                            solution_sort = np.unique(np.sort(abs(solution)))
                            solution_sort = np.array(solution_sort)
                            StrSol = np.array2string(solution_sort)

                            df = df.append(
                                {
                                    "l": x,
                                    "k": y,
                                    "solution": solution,
                                    "solutionStr": StrSol,
                                    "gcd": gcd,
                                },
                                ignore_index=True,
                            )

    df.sort_values("gcd", inplace=True)
    # Se borran los valores duplicados (manteniendo el primer valor)
    df.drop_duplicates(subset="solutionStr", keep="first", inplace=True)
    df = df.reset_index(drop=True)
    df.dropna()

    df.to_json('df.json', orient='records')

    return df
