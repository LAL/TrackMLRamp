#!/usr/bin/env python2.7
# benchmark.py
# Thomas Boser

#10000 particles generated in 0.533506155014 seconds.
#hits for 10000 particles computed in 0.0217640399933 seconds.

import particleController as pc
import time

def benchmarkPC(n):
	cont = pc.particleController()
	start = time.time()
	cont.createParticles(10000)
	end = time.time()
	print n, "particles generated in", end-start, "seconds."

	start = time.time()
	cont.computeallHits()
	end = time.time()
	print "hits for", n, "particles computed in", end-start, "seconds."

benchmarkPC(10000)