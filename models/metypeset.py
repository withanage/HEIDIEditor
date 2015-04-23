import os
import shutil
from subprocess import Popen, PIPE, check_call  ,check_output
import uuid
import time

def metypeset_conversion(filename):
    app_path = '/home/www-data/web2py/applications/HEIDIEditor/'
    retcode=''
    metypeset_path = app_path+'static/meTypeset/bin/meTypeset.py'
    upload_folder = 'uploads'
    file_prefix = filename.rsplit('.', 1)[0]
    file_type = filename.rsplit('.', 1)[1]
    
    file_path  =app_path+ upload_folder+'/'+filename
    
    directory_path  = app_path + upload_folder+'/'+file_prefix
    
    cmd = 'python '+metypeset_path +' '+ file_type +' '+file_path+' '+ directory_path
    if  not os.path.exists(directory_path) :
		retcode = directory_path +' does not exist'
	
    try:
		p = Popen(cmd, shell=True, stdin=PIPE)
		time.sleep(10)
		src_dir = directory_path+'/nlm/out.xml'
		dst_dir =  app_path + upload_folder+'/'+file_prefix+'_nlm.xml'
		shutil.move(src_dir, dst_dir)
		
		src_dir = directory_path+'/tei/out.xml'
		dst_dir =  app_path + upload_folder+'/'+file_prefix+'_tei.xml'
		
		shutil.move(src_dir, dst_dir)
		
		
		
        
		
		
		
    except OSError as e:
        retcode = [cmd, e]
    return dict(retcode=retcode)



def sudo(command, password=None, prompt="Enter password "):

	import pexpect

	if not password:
		import getpass
		password = getpass.getpass(prompt)

		command = "sudo " + command
		child = pexpect.spawn(command)
		child.expect(['ssword', pexpect.EOF])
		child.sendline(password)
		child.expect(pexpect.EOF)
		child.close() 
