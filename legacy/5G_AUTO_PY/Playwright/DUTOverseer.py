#   Anthony Tang
#   Anthony.Tang@nokia.com

#standard library imports
#third party imports
import scp
import paramiko
#local imports



class DUTOverseer():

    def __init__(self, hostname="127.0.0.1",
                port=2001,
                un="root",
                pwd='umniedziala'):

        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print("Attempting to connect to: ")
        print(hostname)
        print(port)

        #try to connection
        try:
            self.ssh.connect(hostname, port = port, username = un,
                            password = pwd)

            #get pseudo terminal look up paramiko
            self.channel = self.ssh.invoke_shell()
            self.pseudoterminal = self.ssh.get_pty()
            print("connection is all good")

        except:
            print("Connection Error ")

    def exec_command(self, command):
        self.channel.send(command)
        buff=''
        while (buff.endswith('$ ')==False and buff.endswith('$  ')==False) :
            resp = self.channel.recv(9999)
            buff += resp

        #chan.close()
        return buff


if __name__ == "__main__":
    ssh = DUTOverseer('192.168.100.1',
                        int('22'),
                        'root',
                        'umniedziala')
    if ssh:
        print("connection successful")
        ssh.exec_command("ls -l")
