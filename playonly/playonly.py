#! /usr/bin/env python
"""playonly takes a ros bag file, and remaps all parameters other than specified to a /null/ namespace

Usage: rosbag <other rosbag params> `playonly <bagfile> /topic1 /topic2 ... /topicN`
Example: rosbag play `playonly.py run2_2018-09-12-21-20-23.bag /scan /tf` 
                will only publish /scan and /tf under their original topic names.

"""
from __future__ import print_function
import sys, os, subprocess, yaml

def playonly():
    if len(sys.argv) < 3:
        sys.stderr.write(__doc__)
        if len(sys.argv) == 1:
            sys.stderr.write("ERROR: missing <bagfile> parameter\n")
        if len(sys.argv) == 2:
            sys.stderr.write("ERROR: need at least one topic to pass through\n")
        sys.exit(1)
    
    bagfile = sys.argv[1] # "bincaddy-run2_2018-09-12-21-20-23.bag"
    playtopics = sys.argv[2:] # ["/scan", "/tf"]

    if not os.path.exists(bagfile):
        sys.stderr.write("ERROR: Bag file '%s' doesn't exist.\n" % bagfile)
        sys.exit(1)

    # Use rosbag info to get topic list
    rosbagcmd = "rosbag info -y -k topics " + bagfile
    bagtopicsinfoyaml = subprocess.check_output(rosbagcmd.split())
    bagtopicsinfo = yaml.load(bagtopicsinfoyaml)
    bagtopics = [t['topic'] for t in bagtopicsinfo]
    #sys.stderr.write(str(bagtopics))

    for t in playtopics:
        if not t in bagtopics:
            sys.stderr.write("ERROR: Topic '%s' isn't in bag.\n" % t)
            sys.exit(1)

    remaps = []
    for t in bagtopics:
        if t not in playtopics:
            #sys.stderr.write(t + " not in " + str(playtopics))
            # e.g. /rosout is remapped as /rosout:=/null/rosout
            remaps.append(t + ":=/null/" + t[1:])

    sys.stdout.write(bagfile + " " + " ".join(remaps))
    sys.exit(0)
