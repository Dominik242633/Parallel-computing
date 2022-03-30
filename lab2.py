from mpi4py import MPI

comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()
p = comm.Get_size()


def oneToAllPersRing(sendMsg, sendSize, recvMsg):
    """sendMsg - processor from we want to send message
    sendSize - number of processors
    recvMsg - to what processor we want to send message"""
    message = ''

    if my_rank == 0:
        for i in range(p-1, 0, -1):
            comm.send(data[i], dest=1)
        message = data[0]

    for i in range(1, p-1):
        if i == my_rank:
            for j in range(1, p-my_rank):
                message = comm.recv(source=my_rank-1)
                comm.send(message, dest=my_rank+1)
            message = comm.recv(source=my_rank-1)

    if my_rank == p-1:
        message = comm.recv(source=my_rank-1)

    print(f"PROC {my_rank} received message {message}")


if my_rank == 0:
    data = [0, 1, 2, 3]

oneToAllPersRing(sendMsg=0, sendSize=p, recvMsg=my_rank)
# print(f"my_Rank: {my_rank}")
# print(f"p: {p}")

MPI.Finalize()
