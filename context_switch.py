#!/usr/bin/env python

log = open('log', 'r')
lines = log.readlines()

context_switch = [] 

for line in lines:
	line = line.strip()
	inst, args = line.split(' ', 1)
	
	if inst == 'switch':
		out_task, in_task, tick, tick_reload, out_minitick, in_minitick = args.split(' ')
		out_time = (float(tick) + (float(tick_reload) - float(out_minitick)) / float(tick_reload)) / 100 * 1000;
		in_time = (float(tick) + (float(tick_reload) - float(in_minitick)) / float(tick_reload)) / 100 * 1000;
		
		overhead = {}
		overhead['out'] = out_task
		overhead['in'] = in_task
		overhead['duration'] = in_time - out_time
		context_switch.append(overhead)
log.close()

cost = open('cost', 'w')
# grasp = open('sched.grasp', w') # maybe grasp could display context switch cost, not yet study
for overhead in context_switch:
	cost.write('switch from %s to %s cost %f seconds\n' % (overhead['out'], overhead['in'], overhead['duration']))
cost.close()
