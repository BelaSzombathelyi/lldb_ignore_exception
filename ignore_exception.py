#! /usr/bin/env python

import lldb

def igonre_objc_exception_throw(debugger, user_input, result, internal_dict):
	target = debugger.GetSelectedTarget()
	thread = target.GetProcess().GetSelectedThread()
	userInputString = str(user_input)
	user_input_parts = userInputString.split()
	for i in range(0, thread.GetNumFrames()):
		frame = str(thread.GetFrameAtIndex(i))
		if frame.find(str(user_input_parts[0])) != -1 and frame.find(str(user_input_parts[1])) != -1:
			output = "Skipping 'Exception' by symbol: 'objc_exception_throw' frame: '{0}'".format(user_input)
			result.PutCString(output)
			result.flush()
			debugger.SetAsync(True)
			debugger.HandleCommand("continue")
			break

def __lldb_init_module(debugger, internal_dict):
	debugger.HandleCommand('command script add -f ignore_exception.igonre_objc_exception_throw ignore')

