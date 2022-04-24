from mpi4py import MPI

comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()
p = comm.Get_size()


def oneToAllPersRing():
    message = ''

    # If process 0, then send messages to 1 process - data from last to first
    if my_rank == 0:
        for i in range(p-1, 0, -1):
            comm.send(data[i], dest=1)
            print(f"PROC 0 sent message {data[i]}")
        message = data[0]

    # For process 1 to p-1 receive from previous process, then send to next process
    for i in range(1, p-1):
        if i == my_rank:
            for j in range(1, p-my_rank):
                message = comm.recv(source=my_rank-1)
                comm.send(message, dest=my_rank+1)
                print(f"PROC {my_rank} received and sent message {message}")
            message = comm.recv(source=my_rank-1)

    # If last process than only receive message
    if my_rank == p-1:
        message = comm.recv(source=my_rank-1)

    print(f"PROC {my_rank} received message {message}")


if my_rank == 0:
    data = [0, 1, 2, 'aaa']

oneToAllPersRing()

MPI.Finalize()
