from mpi4py import MPI

comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()
p = comm.Get_size()

if my_rank == 0:
    number_to_send = 5
    comm.send(number_to_send, dest=1)
    print(f"PROC 0: Sending number {number_to_send}")
if my_rank == 1:
    received_number = comm.recv(source=0)
    print(f"PROC 1: Received number {received_number}")

MPI.Finalize()
