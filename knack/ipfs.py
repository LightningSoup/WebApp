# A basic implementation of IPFS in Python, since there isn't a standard
# one under the IPFS repository at https://github.com/ipfs/
# This basically just defines a list of functions that execute their respective
# IPFS subcommand using the Python subprocess.check_output() function.
# Example:
# >>> import ipfs
# >>> hash = ipfs.add(filename) # Executes `ipfs add <filename>` and saves
#                                 the resulting hash in `hash`

import ipfsapi
import socket

def add_string(str):
    api_ip = socket.gethostbyname('127.0.0.1')
    ipfs_api_obj = ipfsapi.Client(host=api_ip, port=5001)
    return ipfs_api_obj.add_str(str)

def add_file_contents(contents):
    # Empty the file before writing to it
    open('.__temp', 'w').close()

    with open(".__temp", "wb") as fp:
        fp.write(contents)
        fp.close()

    api_ip = socket.gethostbyname('127.0.0.1')
    ipfs_api_obj = ipfsapi.Client(host=api_ip, port=5001)
    return ipfs_api_obj.add(".__temp")["Hash"]

def cat(rcs_hash):
    api_ip = socket.gethostbyname('127.0.0.1')
    ipfs_api_obj = ipfsapi.Client(host=api_ip, port=5001)
    return ipfs_api_obj.cat(rcs_hash)
