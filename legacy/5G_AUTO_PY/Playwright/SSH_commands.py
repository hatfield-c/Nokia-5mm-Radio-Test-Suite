import scp
import paramiko
import time
import subprocess
import os


class SSH(object):

    def __init__(self, hostname="127.0.0.1", port=2001, un="root",pwd='umniedziala',display_window=None):

        try:
            out=subprocess.check_output("ping -n 1 -w 1000 %s"%hostname,shell=True)
        except:
            out=''
            raise Exception("no ping to unit")
            return

        self.display_window=display_window
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(hostname)
        print(port)
        try:

            self.ssh.connect(hostname,port=port,username=un,password=pwd)
            self.chan = self.ssh.invoke_shell()
        except:
            print ("connection error")


    def close(self):
        self.client.close()


    def exec_command(self, command,look_4='$ ',):
        if self.display_window !=None:self.display_window.Print( '--> '+command)
        self.chan.send(command)
        buff=''
        while (buff.endswith('$ ')==False and buff.endswith('$  ')==False) :
            resp = self.chan.recv(9999)
            buff += resp

        if self.display_window !=None:self.display_window.Print( '<-- '+buff)
        #chan.close()
        return buff


    def write(self, command):
        return self.exec_command(command)


    def read(self, command):
        return self.exec_command(command)


    def upload(self, local_file, remote_file):
#        import scp
        scp_instance = scp.SCPClient(self.ssh.get_transport())
        scp_instance.put(local_file, remote_file)


    def download(self, remote_file, local_file):
#        import scp
        scp_instance = scp.SCPClient(self.ssh.get_transport())
        scp_instance.get(remote_file, local_file)


    def uploadNeededFiles(self,inunit,path2uploadfiles):

        #print inunit
        for files in os.listdir(path2uploadfiles):
            #print files
            if files not in inunit:
                #if not os.path.isdir(path2uploadfiles+'\\'+files):
                print("uploading file: %s" %files)
                self.upload(path2uploadfiles+'\\'+files,'/mnt/'+files)


if __name__ == '__main__':
    ssh = SSH_commands.SSH('192.168.100.1',int('22'),'root','umniedziala')
    if ssh:
        print("connection successful")
