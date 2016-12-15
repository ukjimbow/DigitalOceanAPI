import requests
import json

"""
TODO:
	- Add ID or name to Total _____ under account 
	- clean up region
	- if total snapshots/backups = 0 dont print next line
	- check if "[-] OS:', item['image']['name'],"     still works when there is 1 droplet 
	- valid check if token is empty or not when going public
	- Choice to output to CSV
"""


token = ''

headers = {
	'Authorization':'Bearer ' + token,
	'Content-Type':'application/json'
}


idNumber = []

def listDroplets(idNumber):
	r = requests.get("https://api.digitalocean.com/v2/droplets", headers=headers)
	headersList = dict(r.headers)

	print '\n[+] Rate limit remaining:', headersList['ratelimit-remaining'], '\n'
	droplets = json.loads(r.text)

	print '[+] Droplets:\n'
	for item in droplets['droplets']:
		idNumber.append(item['id'])		
		print '   [+] Name:', item['name']
		print '   [-] Status:', item['status']
		print '   [-] OS:', item['image']['name'], '\n'		# I believe it was ['kernel']['image'] if there was 1 droplet but not 100% sure

listDroplets(idNumber)



####################################################################################

def listAccount(idNumber):
	r2 = requests.get("https://api.digitalocean.com/v2/account", headers=headers)
	accountResponse = r2.text
	jsonAccount = json.loads(accountResponse)
	accountInfo2 = dict(jsonAccount)
	accountData = accountInfo2['account']
	
	print '[+] Account:\n'
	print '   [-] Status: ', accountData['status']
	print '   [-] Status message: ', accountData['status_message'], '\n'

listAccount(idNumber)

####################################################################################

def listSnapshots(idNumber):

	for num in idNumber:
		#print 'inside number:', num
		#print 'URL' + str(num)
		
		r3 = requests.get("https://api.digitalocean.com/v2/droplets/" + str(num) + "/snapshots?page=1&per_page=1", headers=headers)
		
		snapshotResponse = r3.text
		jsonSnapshot = json.loads(snapshotResponse)
		total = jsonSnapshot['meta']						# We are able to use this format due to it is first on the list unlike "snapshots" below where we have to use for loop
		print '[+] Total', num, 'snapshots:', total['total'], '\n'

		print '[+]', num, 'snapshots:\n'
		for snapshots in jsonSnapshot['snapshots']:
			print '   [+] Snapshot:', snapshots['name']
			print '   [-] Created:', snapshots['created_at']
			print '   [-] Region:', snapshots['regions'], '\n'
		

listSnapshots(idNumber)



####################################################################################

def listBackups(idNumber):
	for num in idNumber:
		#print 'inside number:', num
		#print 'URL' + str(num)

		r4 = requests.get("https://api.digitalocean.com/v2/droplets/" + str(num) + "/backups", headers=headers)

		backupResponse = r4.text
		jsonBackups = json.loads(backupResponse)

		totalB = jsonBackups['meta']						
		print '[+]', num, 'total backups:', totalB['total'], '\n'

		print '[+]', num,' backups:\n'
		for backups in jsonBackups['backups']:
			print '   [+] Name:', backups['name']
			print '   [-] Created:', backups['created_at']
			print '   [-] Region:', backups['regions']
			print '   [-] Size:', backups['size_gigabytes'], '\n'

listBackups(idNumber)























