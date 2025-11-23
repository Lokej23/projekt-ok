# Problem 1: TSP z ograniczeniem czasu i paliwa

Problem komiwojażera (*Traveling Salesman Problem*), w którym przedstawiciel handlowy musi również przejmować się kosztami paliwa i ramami czasowymi.

## Model matematyczny

### Dane

* $V = \{0,1,...,n-1\}$ – zbiór miast (wierzchołków)
* $c_{ij}$ – Odległość/koszt przejazdu między miastami $i$ i $j$
* $t_{ij}$ – Czas przejazdu z $i$ do $j$
* $[e_i, l_i]$ – Okno czasowe dla miasta $i$
* $a,b$ – Parametry funkcji kosztu paliwa
* $M$ – Stała (duża liczba)

### Funkcja celu

Funkcja polega na zminimalizowaniu łącznego kosztu:

$$
\min Z = \sum_{i=0}^{n-1} \sum_{j=0}^{n-1}(c_{ij}+f_{ij}) \cdot x_{ij} + \sum_{i=0}^{n-1} P_i
$$

Dodatkowo koszt paliwa dla odcinka $i \rightarrow j$:

$$
f_{ij} = a \cdot c_{ij} + b \cdot c_{ij}^2
$$

### Ograniczenia

**1. Każde miasto odwiedzone dokładnie raz:**

$$
\sum_{i=0}^{n-1} x_{ij} = 1, \quad \forall j = 0,1,...,n-1
$$

$$
\sum_{j=0}^{n-1} x_{ij} = 1, \quad \forall i = 0,1,...,n-1
$$

**2. Eliminacja podcykli (MTZ):**

$$
u_i - u_j + n \cdot x_{ij} \le n-1, \quad \forall i,j = 1,2,...,n-1
$$

$$
u_0 = 0
$$

**3. Ograniczenia czasowe i kara:**

$$
T_j \ge T_i + t_{ij} - M(1-x_{ij}), \quad \forall i \ne j, \; i,j \in V
$$

$$
e_i \le T_i \le l_i + P_i, \quad \forall i \in V
$$

### Zmienne decyzyjne

* $x_{ij} \in \{0,1\}$ dla $i,j \in V$
* $T_i \in \mathbb{R}$ – Czas przybycia w mieście $i$
* $P_i \in \mathbb{R}$ – Kara za spóźnienie w mieście $i$
* $u_i \in \mathbb{Z}$ – Zmienne pomocnicze do eliminacji podcykli
