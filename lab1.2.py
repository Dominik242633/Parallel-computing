from mpi4py import MPI

comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()
p = comm.Get_size()

if my_rank == 0:
    number_to_send = 5
    comm.send(number_to_send, dest=1)
    print(f"PROC 0: sending number {number_to_send}")
    received_number = comm.recv(source=1)
    print(f"PROC 0: Received number {received_number}")
if my_rank == 1:
    received_number = comm.recv(source=0)
    print(f"PROC 1: received number {received_number}")
    received_number += 3
    print(f"PROC 1: Adding number 3 and sending number {received_number}")
    comm.send(received_number, dest=0)

MPI.Finalize()
