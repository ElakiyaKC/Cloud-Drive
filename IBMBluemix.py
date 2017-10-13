#!/usr/bin/env python
import swiftclient
import os
import bz2
from dateutil import parser
import datetime
#Credentials intialization
auth_url = "####"
password = "####"
project_id = "####"
user_id = "####"
region_name = "dallas"

#Establishing connection to the Web application
conn = swiftclient.Connection(key=password,authurl=auth_url,auth_version='3',os_options={"project_id":project_id,"user_id":user_id,"region_name":region_name})

#creating the containers
cont_name='Folder1'
conn.put_container(cont_name)

print("Operations available:\n")
print("1.Upload\n2.Download\n3.List\n4.Delete\n5. Delete file with time constraint")
response=input("Enter your choice:")
if(response==1):
	#Calculate the size of the container
	size=0
	for data in conn.get_account()[1]:  #goes to bluemix account
		for data in conn.get_container('Folder1')[1]:
			size+=len(conn.get_object('Folder1',data['name'])[1])
	print ("The size of the container is:")
	print size
	with open('test1.txt','rb') as fs:
		fs.seek(0, os.SEEK_END)
		new_file_size=fs.tell()
		print ("New file size:")
		print str(new_file_size)


	#uploading plain file
	if(size+new_file_size>10000000 and new_file_size>1000000 ):
		print ("Maximum size exceeded")
	else:
		print("Size of the container is less than 10MB")
		print("Which file do you want to upload:")
		print("1.Plain\n2.Encrypt")
		upload_choice=input("Enter your choice")
		if(upload_choice==1):
			with open('test1.txt','rb') as f:
				plain_content=f.read()
				conn.put_object(cont_name,"test1.txt",contents=plain_content,content_type='text/plain')
				print("File uploaded successfully")
				f.close()
				
				
			
		elif(upload_choice==2):
			#uploading encrypted file
			with open('test2.txt','rb') as ef:
				content1=ef.read()
				encrypted_content=bz2.compress(content1)
				print("Encryption sucessful")
				conn.put_object(cont_name,"test2.txt",contents=encrypted_content,content_type='text/plain')
				print("Encrypted file uploaded successfully")
				ef.close()
		else:
			print("Please enter a valid choice\n")
		
elif(response==2):
	print("Which file do you want to upload:")
	print("1.Plain\n2.Encrypt")
	download_choice=input("Enter your choice")
	if(download_choice==1):
		#download file from the container(plain file)
		object=conn.get_object('Folder1','test1.txt')
		with open('plainfile_download1.txt','w+') as f1:
			f1.write(object[1])
			print("File downloaded successfully")
		
	elif(download_choice==2):
		#download file from the container(encrypted file)
		obj=conn.get_object('Folder1','test2.txt')
		with open('Decrypt_download.txt','w+') as file1:
			file1.write(bz2.decompress(obj[1]))
			print("File decrypted successfully")
			
	else:
		print("Please enter a valid option")
		
elif(response==3):
	#List the files in the container
	for data in conn.get_container('Folder1')[1]:
			print ('Object name : {0} \nSize: {1} \nDate: {2}\n'.
                 format(data['name'], data['bytes'], data['last_modified']))
	
elif(response==4):
	print("Delete the \n1.Remote file\n2.File from cloud")
	choice=input("Enter thr option")
	if(choice==2):
		#Delete a file from the container
		conn.delete_object('Folder1','File1.txt' )
		print ("File deleted successfully")
	elif(choice==1):
		#Delete remote file
		os.remove("delete.txt")
		print("Remote file deleted")
	else:
		print("Enter a valid option")
	
elif(response==5):
	#Calculate time
	minutes = input("enter the time")
	for data in conn.get_container('Folder1')[1]:
		date=data['last_modified']
		date1=parser.parse(date)
		subtract=datetime.timedelta(0,minutes*60)
		current_date=datetime.datetime.utcnow()-datetime.timedelta(0,minutes*60)
		if(date1<=current_date):
			conn.delete_object('Folder1',data['name'])
			print("File has been deleted")
		else:
			print("No files were uploaded before after the given time")

else:
	print("Enter a valid choice")