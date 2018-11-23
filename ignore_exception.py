#! /usr/bin/env python

import lldb

def call_continue(debugger):
	debugger.SetAsync(True)
	debugger.HandleCommand("continue")
	return None

def thread_is_on_objc_exception_throw_symbol(thread):
	return thread.GetFrameAtIndex(0).symbol.name.find('objc_exception_throw') != -1

def find_frame_by_user_input(thread, user_input):
	user_input_parts = str(user_input).split()
	for i in range(0, thread.GetNumFrames()):
		frame = thread.GetFrameAtIndex(i)
		frameString = str(frame)
		if frameString.find(user_input_parts[0]) != -1 and frameString.find(user_input_parts[1]) != -1:
			return frame
	return None

def need_igonre_objc_exception_throw(debugger, user_input):

	thread = debugger.GetSelectedTarget().GetProcess().GetSelectedThread()

	#print("Thread name: " + str(thread.GetName()))
	#print("Queue name: " + thread.GetQueue().GetName())
	
	#Skip Google analitics GAIThread
	thread_name = thread.GetName()
	if thread_name != None and thread_name.find("GAIThread") != -1:
		return "'GAIThread' found in thread name!"
	

	# Skip only on 'objc_exception_throw' symbol
	if not thread_is_on_objc_exception_throw_symbol(thread):
		return None

	# Iterate on frame stack to found the match by 'user_input'
	frame = find_frame_by_user_input(thread, user_input)
	if frame != None:
		return "Skipping 'Exception' by frame: '{0}'".format(frame.GetFunctionName())

	return None

def igonre_objc_exception_throw(debugger, user_input, result, internal_dict):
	skip_text = need_igonre_objc_exception_throw(debugger, user_input)
	if skip_text != None:
		result.PutCString(skip_text)
		result.flush()
		call_continue(debugger)
	return None

def __lldb_init_module(debugger, internal_dict):
	#command script add -f {file name}.{function name} {alias}
	debugger.HandleCommand('command script add -f ignore_exception.igonre_objc_exception_throw ignore')

