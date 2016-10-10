#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
sys.path.insert(0, "../")

import aiml

# The Kernel object is the public interface to
# the AIML interpreter.
k = aiml.Kernel()
# Use the 'learn' method to load the contents
# of an AIML file into the Kernel.
k.learn("cn-test2.aiml")
# Use the 'respond' method to compute the response
# to a user's input string.  respond() returns
# the interpreter's response, which in this case
# we ignore.

# Loop forever, reading user input from the command
# line and printing responses.
while True: 
	a = raw_input("> ").decode(sys.stdin.encoding)
	print k.respond(a.encode('utf-8'))