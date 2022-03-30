from mpi4py import MPI

def f(x):
    return x*x

def Trap(a, b, n, h):
    integral = (f(a) + f(b))/2.0

    x = a
    for i in range(1, int(n)):
        x = x + h
        integral = integral + f(x)

    return integral * h


comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()
p = comm.Get_size()

a = 0.0
b = 1.0
n = 1024
dest = 0
total = -1

h = (b-a)/n
local_n = n/p
local_a = a + my_rank*local_n*h
local_b = local_a + local_n*h
integral = Trap(local_a, local_b, local_n, h)

if my_rank == 0:
    total = integral
    for source in range(1, p):
        integral = comm.recv(source=source)
        print(f"PE {my_rank} <- {source}, {integral} \n")
        total = total + integral
else:
    print(f"PE {my_rank} -> {dest}, {integral} \n")
    comm.send(integral, dest=0)

if my_rank == 0:
    print(f"With n={n}, trapezoids, \n")
    print(f"integral from {a} to {b} = {total} \n")

MPI.Finalize()
