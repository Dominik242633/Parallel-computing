from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()
p = comm.Get_size()

random_number = np.random.randint(0, 10)

if my_rank == 0:
    print(f"PROC 0: sending number {random_number}")
    comm.send(random_number, dest=1)
    received_number = comm.recv(source=3)
    print(f"PROC 0: Received number {received_number}")
elif my_rank == 1:
    received_number = comm.recv(source=0)
    print(f"PROC 1: received number {received_number}")
    number_to_send = received_number + random_number
    print(f"PROC 1: sending number {number_to_send}")
    comm.send(number_to_send, dest=2)
elif my_rank == 2:
    received_number = comm.recv(source=1)
    print(f"PROC 2: received number {received_number}")
    number_to_send = received_number + random_number
    print(f"PROC 2: sending number {number_to_send}")
    comm.send(number_to_send, dest=3)
elif my_rank == 3:
    received_number = comm.recv(source=2)
    print(f"PROC 3: received number {received_number}")
    number_to_send = received_number + random_number
    print(f"PROC 3: sending number {number_to_send}")
    comm.send(number_to_send, dest=0)

MPI.Finalize()
