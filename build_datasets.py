#!/usr/bin/env python2.7
# build_datasets.py
# Thomas Boser

"""
Basic command line program to create datasets.

Example usage:
python2.7 build_datasets.py --output-dir /path/to/outdir/ --num-events 10 --hits-per-event 10000 
"""

import os
import random
import argparse
import Generation.particleController as pc

class DatasetGenerator:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Generates TrackML datasets and solutions.')
        parser.add_argument('--output-dir', default='/', required=False)
        parser.add_argument('--num-events', default=1, required=False)
        parser.add_argument('--hits-per-event', default=1000, required=False)
        parser.add_argument('--detectors', default=range(1000, 8001, 1000), required=False) #not implmented yet

        args = parser.parse_args()
        self.outdir = args.output_dir
        self.numevents = int(args.num_events)
        self.hpe = int(args.hits_per_event)
        self.detectors = args.detectors

        self.generateDataset()

    def generateDataset(self):
        """ create a directory with new dataset based on specs """
        if self.outdir[-1] != "/": 
            self.outdir += "/"
        self.outdir += "dataset_trackml"
        i = 1
        while os.path.exists(self.outdir):
            self.outdir += ("_"+str(i))
            i += 1
        cmd = "mkdir -p "+ self.outdir
        os.system(cmd)

        cont = pc.particleController()
        cont.generateEvents(self.numevents, self.hpe, self.detectors)

        self.generateHits(cont)
        self.generateTruths(cont)
        self.generateSolution(cont)

    def generateHits(self, cont):
        """ generates the hits.csv file """
        hitf = self.outdir + "/hits.csv"
        old = os.dup(1)
        os.close(1)
        os.open(hitf, os.O_WRONLY | os.O_CREAT)
        cont.printallHits()
        os.close(1)
        os.dup(old)
        os.close(old)

        lines = open(hitf).readlines()
        random.shuffle(lines)
        open(hitf, 'w').writelines(lines)

    def generateTruths(self, cont):
        """ generates the tracks.csv file """
        truthf = self.outdir + "/tracks.csv"
        old = os.dup(1)
        os.close(1)
        os.open(truthf, os.O_WRONLY | os.O_CREAT)
        cont.printallTruths()
        os.close(1)
        os.dup(old)
        os.close(old)

    def generateSolution(self, cont):
        """ generates the tracks_soln.csv file """
        solnf = self.outdir + "/tracks_soln.csv"
        old = os.dup(1)
        os.close(1)
        os.open(solnf, os.O_WRONLY | os.O_CREAT)
        cont.printallSolutions()
        os.close(1)
        os.dup(old)
        os.close(old)

if __name__ == '__main__':
    dg = DatasetGenerator()