sira = Queue()


def worker(q):
    while True:
        q = sira.get()
        connectionkapici(q)
        sira.task_done()


def sshThread():
    with open('connection_iplist_10.txt') as f:
        content = f.readlines()
    ip_list = [x.strip() for x in content]

    for i in range(1):
        trd = threading.Thread(target=worker, args=(sira,))
        trd.setDaemon(True)
        trd.start()

    for ip in ip_list:
        sira.put(ip)
    sira.join()


if __name__ == '__main__':
    sshThread()
