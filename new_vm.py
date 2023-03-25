import subprocess
import random


def create(cpu: str = 'host',
           threads: int = 1,
           sockets: int = 1,
           cores: int = 1,
           memory: int = 1024,
           hd_files: list = None,
           floppy_files: list = None,
           qmp: str = None,
           noGUI: bool = True,
           extra_args: str = ''):
    cmd = 'qemu-system-x86_64'
    if qmp:
        cmd += f'{qmp}'

    # Configure memory and cpu
    cmd += f' -cpu {cpu}'
    cmd += f' -m {memory}'
    cpus = sockets * cores * threads
    cmd += f' -smp cpus={cpus},sockets={sockets},cores={cores},threads={threads}'

    if hd_files:
        assert len(hd_files) <= 4, "four disk max!"
        hd_name = ['hda', 'hdb', 'hdc', 'hdd']
        for i in range(len(hd_files)):
            cmd += ' -{hd_name} "{hd_path}"'.format(hd_name=hd_name[i], hd_path=hd_files[i])

    if floppy_files:
        assert len(floppy_files) <= 2, "four disk max!"
        floppy_name = ['fda', 'fdb']
        for i in range(len(floppy_files)):
            cmd += ' -{hd_name} "{hd_path}"'.format(hd_name=floppy_name[i], hd_path=floppy_files[i])

    if noGUI:
        cmd += ' -nographic'

    if extra_args:
        cmd += f' {extra_args}'

    # print(cmd)
    return subprocess.Popen(cmd, shell=True, stdin=None,
                            stdout=None, stderr=None, close_fds=True).pid


def qmp_tcp(
        addr: str = 'localhost',
        port: int = 4501):
    return f' -qmp tcp:{addr}:{port},server,wait=off'


def qmp_unix(
        sockFile: str = None):
    return f' -qmp unix:"{sockFile}",server=on,wait=off'


def gen_mac():
    chars = [i for i in range(0, 10)]
    for i in ['A', 'B', 'C', 'D', 'E', 'F']:
        chars.append(i)
    mac = ''
    for i in range(12):
        temp = random.choice(chars)
        if i % 2 != 0 and (temp.__class__ == int and (temp % 2 != 0)):
            temp = random.choice([i for i in range(2, 9, 2)])

        if (i != 0 and i != 1) and i % 2 == 0:
            print(1, i, temp)
            mac += ':' + str(temp)
        elif i != 0 and i != 1:
            print(2, i, temp)
            mac += str(temp)
        else:
            print(3, i, temp)
            mac += str(temp)

    return mac
