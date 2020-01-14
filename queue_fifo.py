from kazoo.client import KazooClient

'''
先进先出队列
在zookeeper中先创建一个根目录 /queue_fifo，做为队列
入队操作就是在queue_fifo下创建自增序的子节点，并把数据放入节点内
出队操作就是先找到queue_fifo下序号最小的那个节点，取出数据，然后删除此节点
'''
hosts = "192.168.45.103:2181"
zk = KazooClient(hosts=hosts)
zk.start()
zk.ensure_path('/queue_fifo')

def getQueue():
    min_child = None
    data = None
    if zk.exists("/queue_fifo"):
        children = zk.get_children("/queue_fifo")
        child_list = sorted(children)
        min_child = child_list[0]
        # print(min_child)
    if min_child != None:
        min_child_path = "/queue_fifo/" + min_child
        try:
            data,stat = zk.get(min_child_path)
            zk.delete(min_child_path)
        except Exception as e:
            print(e)
    return data.decode()

def putQueue(data): #000001   /queue_fifo/000001
    if not zk.exists("/queue_fifo"):
        zk.ensure_path("/queue_fifo")
    zk.create("/queue_fifo/%s"%data, b"%s"%data.encode())
