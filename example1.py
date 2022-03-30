# Send the data
# comm.send(self, obj, int dest, int tag=0)
# obj - object you sending (containing data to be sent)
# dest - number of process where you want this information to go
# tag - (optional) number, which allows to distinguish among messages

# Receive the data
# comm.recv(self, buf=None, int source=ANY_SOURCE, int tag=ANY_TAG, Status status=None)
# obj - object containing data to be received
# source - which process are you receiving this data from
# tag - (optional) number, which allows to distinguish among messages
# status - (optional) query data about message
# if you invoke receive call, your program will stop until it receives message

# return the number of this process
# comm.Get_rank(self)

# return how many process there are
# comm.Get_size(self)

# Command to run program from cmd
# mpiexec -n 4 python example1.py

from mpi4py import MPI

comm = MPI.COMM_WORLD

my_rank = comm.Get_rank()
p = comm.Get_size()

if my_rank != 0:
    message = f'Hello from {my_rank}'
    comm.send(message, dest=0)
else:
    for procid in range(1, p):
        message = comm.recv(source=procid)
        print(f"Process 0 receives message from process {procid}: {message}")
