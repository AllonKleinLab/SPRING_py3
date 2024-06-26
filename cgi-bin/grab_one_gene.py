#!/usr/bin/env python3

from get_stdin_data import get_stdin_data
import time

t00 = time.time()
def update_log(fname, logdat, overwrite=False):
	if overwrite:
		o = open(fname, 'w')
	else:
		o = open(fname, 'a')
	o.write(logdat + '\n')
	o.close()
def strfloat(x):
    if x == 0: return "0"
    else: return "%.1f" %x
logf = 'tmplog2'

t0 = time.time()
import numpy as np
t1 = time.time()
update_log(logf, 'import numpy -- %.3f' %(t1-t0))

t0 = time.time()
import h5py
t1 = time.time()
update_log(logf, 'import h5py -- %.3f' %(t1-t0))

t0 = time.time()
data, running_cgi = get_stdin_data()
t1 = time.time()
update_log(logf, 'data, running_cgi = get_stdin_data() -- %.3f' %
           (t1-t0), True)

t0 = time.time()
base_dir = data.get_required_dir('base_dir')
sub_dir = data.get_required_dir('sub_dir')
gene = data.get_required('gene')
t1 = time.time()
update_log(logf, 'got cgi data -- %.3f' %(t1-t0))
update_log(logf, gene)

t0 = time.time()
# cell_filter = np.array(map(int, data.get('cell_filter').split(',')))
cell_filter =  np.load(sub_dir + '/' + 'cell_filter.npy')
t1 = time.time()
update_log(logf, 'got cell filter-- %.3f' %(t1-t0))


#t0 = time.time()
#cell_filter = np.loadtxt(sub_dir + '/cell_filter.txt', dtype=int)
##full_cell_filter = np.loadtxt(base_dir + '/cell_filter.txt', dtype=int)
#t1 = time.time()
#update_log(logf, 'loaded cell filters -- %.3f' %(t1-t0))
#update_log(logf, str(len(cell_filter)))
#update_log(logf, str(len(cf)))
#update_log(logf, str(np.all(cf == cell_filter)))

t0 = time.time()
hf = h5py.File(base_dir + '/counts_norm_sparse_genes.hdf5', 'r')
counts = np.array(hf.get('counts').get(gene))
cell_ix = np.array(hf.get('cell_ix').get(gene))
ncells = hf.attrs['ncells']
hf.close()
t1 = time.time()
update_log(logf, 'loaded hdf5 data -- %.3f' %(t1-t0))

t0 = time.time()
#E = np.zeros(len(full_cell_filter), dtype=float)
E = np.zeros(ncells, dtype=float)
t1 = time.time()
update_log(logf, 'inialized array -- %.3f' %(t1-t0))

t0 = time.time()
E[cell_ix] = counts
t1 = time.time()
update_log(logf, 'filled array -- %.3f' %(t1-t0))

t0 = time.time()
E = E[cell_filter]
t1 = time.time()
update_log(logf, 'filtered array -- %.3f' %(t1-t0))

t0 = time.time()
if running_cgi:
	print("Content-Type: text/plain")
	print()
print('\n'.join(map(strfloat,E)))
t1 = time.time()
update_log(logf, 'returned data -- %.3f' %(t1-t0))

t11 = time.time()
update_log(logf, str(t11-t00))
