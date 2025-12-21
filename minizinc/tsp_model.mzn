int: n; 
float: a; 
float: b; 
float: M;
array[int, int] of float: c_matrix; 
array[int, int] of float: t_matrix; 
array[int, int] of float: t_windows;

% indeksowanie od 0 do n-1
set of int: V = 0..n-1;

array[V, V] of float: c = array2d(V, V, [ c_matrix[i, j] | i in 1..n, j in 1..n ]);
array[V, V] of float: t = array2d(V, V, [ t_matrix[i, j] | i in 1..n, j in 1..n ]);
array[V] of float: e = array1d(V, [ t_windows[i+1, 1] | i in V ]);
array[V] of float: l = array1d(V, [ t_windows[i+1, 2] | i in V ]);
array[V, V] of float: f = array2d(V, V, [ 
    a * c[i,j] + b * (c[i,j] * c[i,j]) 
    | i in V, j in V 
]);
array[V, V] of var 0..1: x;
array[V] of var float: T;
array[V] of var float: P;
array[V] of var 0..n: u;
var float: Z;
constraint Z = sum(i in V, j in V)( (c[i,j] + f[i,j]) * x[i,j] ) 
             + sum(i in V)( P[i] );

solve minimize Z;

% Ograniczenia:
% Każde miasto odwiedzone dokładnie raz
constraint forall(j in V) ( 
    sum(i in V) (x[i,j]) = 1 
);
constraint forall(i in V) ( 
    sum(j in V) (x[i,j]) = 1 
);

% brak pętli własnych
constraint forall(i in V) (x[i,i] = 0);

% Eliminacja podcykli (MTZ)
constraint forall(i in 1..n-1, j in 1..n-1 where i != j) (
    u[i] - u[j] + n * x[i,j] <= n - 1
);
constraint u[0] = 0;
constraint forall(i in 1..n-1) (u[i] >= 1 /\ u[i] <= n-1);

% Ograniczenia czasowe i kara
constraint forall(i in V, j in V where i != j /\ j != 0) (
    T[j] >= T[i] + t[i,j] - M * (1 - x[i,j])
);
constraint forall(i in V) (
    T[i] >= e[i] /\
    T[i] <= l[i] + P[i] /\
    P[i] >= 0.0
);
constraint T[0] >= e[0];

% output [ "Z: ", show(Z) ];