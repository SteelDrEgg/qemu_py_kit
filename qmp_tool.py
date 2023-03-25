import socket

commands = [
    'query-cpus-fast',
    'query-machines',
    'query-current-machine',
    'query-uuid',
    'query-vm-generation-id',
    'system_reset',
    'system_powerdown',
    'system_wakeup',
    'inject-nmi',
    'query-kvm',
    'memsave',
    'pmemsave',
    'query-memdev',
    'query-hotpluggable-cpus',
    'set-numa-node',
    'balloon',
    'query-balloon',
    'query-memory-size-summary',
    'query-memory-devices',
    'x-query-irq',
    'x-query-jit',
    'x-query-numa',
    'x-query-opcount',
    'x-query-profile',
    'x-query-ramblock',
    'x-query-rdma',
    'x-query-roms',
    'x-query-usb',
    'dumpdtb',
    'query-cpu-model-comparison',
    'query-cpu-model-baseline',
    'query-cpu-model-expansion',
    'query-cpu-definitions'
]

class qmpClient():
    def __init__(self, qmp_capabilities_mode: bool = False, recv_size: int = 104857600):
        self.recv_size = recv_size
        self.qmp_capabilities_mode = qmp_capabilities_mode

    def init(self):
        self.greeting = self.conn.recv(self.recv_size)
        if not self.qmp_capabilities_mode:
            self.exe(cmd='qmp_capabilities')

    def conn_unix(self, sock_file: str):
        self.conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.conn.connect(sock_file)
        self.init()

    def conn_tcp(self, address: tuple):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(address)
        self.init()

    def exe(self, cmd: str, args: dict = None) -> str:
        command = '{"execute":"%s"' % cmd
        if args:
            command += ', "arguments": %s}' % str(args)
            command.replace("'", '"')
        else:
            command += '}'
        self.conn.send(command.encode('utf-8'))
        return self.conn.recv(self.recv_size).decode('utf-8')

    def shutdown(self):
        self.exe('system_powerdown')
        return True