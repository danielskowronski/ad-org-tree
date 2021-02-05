import argparse, keyring
from getpass import getpass
from ldap3 import Server, Connection, SAFE_SYNC
from pprint import pprint

parser = argparse.ArgumentParser(description='AD Org Tree')
parser.add_argument('server',  type=str)
parser.add_argument('domain',  type=str)
parser.add_argument('username',type=str)
parser.add_argument('path',    type=str)
args = parser.parse_args()

password=keyring.get_password('adot_ldap_pass',args.username)
if password==None:
	password=getpass("Password for %s\\%s: "%(args.domain,args.username))
	keyring.set_password('adot_ldap_pass',args.username,password)

server = Server(args.server)
conn = Connection(server, "%s\\%s"%(args.domain,args.username), password, client_strategy=SAFE_SYNC, auto_bind=True)
status, result, response, _ = conn.search(args.path, '(objectclass=person)')  
pprint(response)