import argparse, keyring
from getpass import getpass
from ldap3 import Server, Connection, SAFE_SYNC
from pprint import pprint

class OrgMember:
	def __init__(self, dn, cn, email, manager_dn):
		self.dn=dn
		self.cn=cn
		self.email=email
		self.manager_dn=manager_dn
	def __str__(self):
		return "User:      %s\n  CN:      %s\n  Mailbox: %s\n  Manager: %s" % (self.dn, self.cn, self.email, self.manager_dn)

parser = argparse.ArgumentParser(description='AD Org Tree')
parser.add_argument('server',  type=str)
parser.add_argument('domain',  type=str)
parser.add_argument('username',type=str)
parser.add_argument('--path',  type=str, nargs='+')
args = parser.parse_args()

password=keyring.get_password('adot_ldap_pass',args.username)
if password==None:
	password=getpass("Password for %s\\%s: "%(args.domain,args.username))
	keyring.set_password('adot_ldap_pass',args.username,password)

server = Server(args.server)
conn = Connection(server, "%s\\%s"%(args.domain,args.username), password, client_strategy=SAFE_SYNC, auto_bind=True)

orgMembers={}

for path in args.path:
	print("Querying %s" % (path))
	status, result, people, _ = conn.search(path, '(objectclass=user)', attributes=['distinguishedName','manager','cn','sAMAccountName','otherMailbox'])  
	for person in people:
		if len(person['attributes']['otherMailbox'])>0:
			mailbox=person['attributes']['otherMailbox'][0]
		else:
			mailbox=''
		orgMember=OrgMember(person['dn'],person['attributes']['cn'],mailbox,person['attributes']['manager'])
		orgMembers.update({person['dn']:orgMember})

for dn,orgMember in orgMembers.items():
	print(orgMember)
