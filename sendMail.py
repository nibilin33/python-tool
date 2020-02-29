# coding: utf-8
import paramiko
import os
import traceback
import shutil
import win32com as win32

host = ""
port = 22
user = ""
password = ""
packageConfig = {
    'web_uc': {
        'local': '', #本地工程路径
        'remote': '', # 目标服务器目录
        'upload': True, # 是否需要发版
        'nextVersionPath': '', # 放包的的地址，直接写下个版本号，会自动创建
    },
    'web_ume': {
        'local': '',
        'remote': '',
        'upload': False,
        'nextVersionPath': '',
    }
}
# 中文要注意编码，u
mailConfig = {
    'receivers':[],
    'subject':u'',
    'mailContentPath':'mail.html', # 邮件模板路径
    # eg:{'mail_path':'J:/python-anaconda/translate.json','file_name':'translate.json'}
    'attachments':[]
}
def __get_all_files_in_local_dir(local_dir):
    all_files = list()
    files = os.listdir(local_dir)
    for x in files:
        filename = os.path.join(local_dir, x)
        if os.path.isdir(filename):
            all_files.extend(__get_all_files_in_local_dir(filename))
        else:
            all_files.append(filename)
    return all_files
def sftp_put_dir(local_dir, remote_dir, sftp, ssh):
    if remote_dir[-1] == '/':
        remote_dir = remote_dir[0:-1]
    print remote_dir
    all_files = __get_all_files_in_local_dir(local_dir)
    for x in all_files:
        filename = os.path.split(x)[-1]
        remote_file = os.path.split(x)[0].replace(local_dir, remote_dir)
        path = remote_file.replace('\\', '/')
        remote_filename = path + '/' + filename
        tdin, stdout, stderr = ssh.exec_command('mkdir -p ' + path)
        print stderr.read()
        print (u'Put文件%s传输到%s中...' % (filename, host))
        sftp.put(x, remote_filename)
def sendOutLook():
    outlook = win32.Dispatch('Outlook.Application')
    mail_item = outlook.CreateItem(0) # 0: olMailItem
    for recipers in mailConfig['receivers']:
        mail_item.Recipients.Add(recipers)
    mail_item.BodyFormat = 2          # 2: Html format
    myfile = open(mailConfig['mailContentPath'], 'r',encoding='utf8')
    for attr in mailConfig['attachments']:
        print attr
        mail_item.Attachments.Add(attr['mail_path'], 1, 1, attr['file_name'])
    data = myfile.read()
    myfile.close()
    mail_item.HTMLBody = data
    mail_item.Subject = mailConfig['subject']
    mail_item.Send()
def package(local, remote, filename, nextVersion):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, user, password)
    sftp = ssh.open_sftp()
    ssh.exec_command('rm -rf ' + remote)
    sftp_put_dir(local, remote, sftp, ssh)
    targetDir = remote[0:remote.rindex('/')]
    targetFile = targetDir + '/' + filename + '.tar.gz'
    ssh.exec_command('rm -rf ' + targetFile)
    tdin, stdout, stderr = ssh.exec_command('cd ' + targetDir + ';' + 'tar -zcvf' + ' ' + filename + '.tar.gz' + ' *')
    print stdout.read()
    print "Downloading files ==> " + targetFile
    localPath = './' + filename + '.tar.gz'
    print localPath
    if os.path.exists(localPath):
        try:
            os.remove(localPath)
            print("File removed successfully")
        except OSError as error:
            print(error)
            print("File path can not be removed")
    sftp.get(targetFile, localPath)
    if not os.path.exists(nextVersion):
        os.mkdir(nextVersion)
    print("Directory ", nextVersion, " Created ")
    shutil.copy(localPath, nextVersion)

if __name__ == '__main__':
    try:
        for itera in packageConfig:
            if packageConfig[itera]['upload']:
                package(packageConfig[itera]['local'], packageConfig[itera]['remote'],itera,packageConfig[itera]['nextVersionPath'])
        sendOutLook()
    except Exception, err:
        print(traceback.format_exc())