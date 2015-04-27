#!/usr/bin/env python

log = open('log', 'r')
lines = log.readlines()

context_switch = [] 
tasks = {}

for line in lines:
	line = line.strip()
	inst, args = line.split(' ', 1)

	if inst == 'task':
		id, priority, name = args.split(' ', 2)
		task = {}
		task['no'] = str(len(tasks) + 1)	# index of task
		task['priority'] = int(priority)
		task['name'] = name.strip()
		task['created'] = True
		task['round'] = 0			# round of execution of this task

		tasks[id] = task			# we can qeury task by id in tasks later
	
	elif inst == 'switch':
		out_task, in_task, tick, tick_reload, out_minitick, in_minitick = args.split(' ')
		out_time = (float(tick) + (float(tick_reload) - float(out_minitick)) / float(tick_reload)) / 100 * 1000;
		in_time = (float(tick) + (float(tick_reload) - float(in_minitick)) / float(tick_reload)) / 100 * 1000;
		
		overhead = {}
		overhead['out'] = out_task
		overhead['in'] = in_task
		overhead['duration'] = in_time - out_time
		context_switch.append(overhead)
	
		out_round = tasks[out_task]['round']
		in_round = tasks[in_task]['round']
		tasks[out_task]['round'] += 1
		tasks[out_task][str(out_round) + 'out'] = out_time   	# record out time of each round the task
		tasks[in_task][str(in_round) + 'in'] = in_time
		
		
log.close()

cost = open('cost', 'w')
# grasp = open('sched.grasp', w') # maybe grasp could display context switch cost, not yet study
for overhead in context_switch:
	cost.write('switch from %s to %s cost %f microseconds\n' % (overhead['out'], overhead['in'], overhead['duration']))
cost.close()


times = open('times', 'w')
for id in tasks:
	r = 0
	try:
		while r < tasks[id]['round']:
			times.write('on %f %s in\n' % (tasks[id][str(r) +'in'], tasks[id]['name']))
			times.write('on %f %s out\n' % (tasks[id][str(r) + 'out'], tasks[id]['name']))
			tasks[id][str(r) + 'elapse'] = tasks[id][str(r) + 'out'] - tasks[id][str(r) + 'in']
			times.write('elapse %f\n' % (tasks[id][str(r) + 'elapse']))
			r += 1
	except:
		pass
times.close()

