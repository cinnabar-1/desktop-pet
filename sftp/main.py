# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import paramiko


def init_ssh():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(hostname="95.169.27.237", port=29211, username="root", password="bwg820gg")
    stdin, stdout, stderr = ssh.exec_command('df -hT ')
    stdin, stdout, stderr = ssh.exec_command('mkdir -p /app/for_out_file/')
    print(stdout.read().decode('utf-8'))
    sftp = ssh.open_sftp()
    return ssh, sftp


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ssh, sftp = init_ssh()
    files = sftp.listdir("/app/for_out_file/")
    # sftp.put()
    # sftp.remove()
    # sftp.put(remotepath="/app/sftp.py",localpath="./main.py")
    # download
    # sftp.get(remotepath="/app/sftp.py",localpath="./main.py")
    print(files)
    sftp.close()
    ssh.close()
