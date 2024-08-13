import mmap
import json
import os
import numpy as np

# Function:
def jb_handle_init():
	N1000 = 40000 # allocated buffer size
	fd = os.open('/tmp/mmWave_FDS', os.O_RDONLY)
	return  mmap.mmap(fd, N1000, mmap.MAP_SHARED, mmap.PROT_READ)

fn = 1
fn_prev = 0

def jb_client_read(mm):
	global fn, fn_prev
	dObj = []
	mm.seek(0)
	data_len = 40
	data = mm.read(data_len)
	a = str(data).split("|")
	fn   = int(a[1]) 
	dlen = int(a[2])
	chk = False
	if fn != fn_prev:
		mm.seek(0)
		read_len = 40 + dlen
		data = mm.read(read_len)
		a = str(data).split("|")
		fn   = int(a[1]) 
		dlen = int(a[2])
		dObj = a[3]
		if len(dObj) > 20:
			chk = True
		fn_prev = fn
	return (chk,fn, dObj)


mm = jb_handle_init()

while True:
	
	(chk, fn, json_data) = jb_client_read(mm)
	if chk:
		data = json.loads(json_data)
		for key in data.keys():
			print(f"\n\n\n###################  {key}   ################")
			print(data[key])
			print("\n======== fdsdata ==========") 
			print(data[key]['fdsdata'])
			print("\n======== object center ==========") 
			print(f"object center:{np.round(data[key]['center'],2)}  state:{data[key]['state']}  cells: {data[key]['fdsdata']['cells']}")


mm.close()
exit()

