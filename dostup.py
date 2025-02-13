import paramiko # этот вроде без сервака не работает 

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname='remote_server', username='username', password='password')

stdin, stdout, stderr = ssh_client.exec_command('ls -l')
print(stdout.read().decode())

ssh_client.close()