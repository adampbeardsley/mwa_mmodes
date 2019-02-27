#!/usr/bin/env python
# Script to unflag uvfits for a given obs
# Will also flag the center channels and band edges
# Also flag last integration

import argparse
import numpy as np
from pyuvdata import UVData
import os
import glob
from hera_qm import xrfi
from hera_qm.metrics_io import process_ex_ants
import sys


a = argparse.ArgumentParser()
a.prog = 'basic_flags.py'
a.add_argument('obses', type=str, nargs='+', help='Observations to unflag')
a.add_argument('--inpath', type=str, default='', help='Path to input data. Default is cwd.')
a.add_argument('--outpath', type=str, default='', help='Path for output. Default is cwd.')
a.add_argument('--ants', type=str, default=None, help='Comma-separated list of antennas to flag')
a.add_argument('--ew', type=int, default=2, help='Coarse channel edge width (each side). default is 2.')
args = a.parse_args()

history = '\n###\n' + ' '.join(sys.argv) + '.  '

ex_ants = process_ex_ants(args.ants)
print('ex_ants = ' + args.ants)

uv = UVData()

for obs in args.obses:
    print('working on obs' + obs)
    files = sorted(glob.glob(os.path.join(args.inpath, obs + '*.uvfits')))
    for filename in files:
        print('\t' + filename)
        outfile = os.path.join(args.outpath, os.path.basename(filename))
        uv.read(filename)
        # Get some metadata
        ncoarse = np.int(np.round((uv.freq_array.max() - uv.freq_array.min()) * 1e-6 / 1.28))
        nfine = uv.freq_array.size
        fine_per_coarse = np.int(nfine / ncoarse)

        uv.flag_array = np.zeros_like(uv.flag_array)
        xrfi.flag_xants(uv, ex_ants)
        dcs = np.arange(fine_per_coarse / 2, nfine, fine_per_coarse)
        print(dcs)
        uv.flag_array[:, :, dcs, :] = True
        for i in range(args.ew):
            chans = np.arange(i, nfine, fine_per_coarse)
            print(chans)
            uv.flag_array[:, :, chans, :] = True
            chans = np.arange(fine_per_coarse - i - 1, nfine, fine_per_coarse)
            print(chans)
            uv.flag_array[:, :, chans, :] = True

        uv.history += history
        uv.write_uvfits(outfile)
