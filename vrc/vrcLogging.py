import time

def logData(info):
	fname = 'VRC_LOG_' + time.strftime("%d_%m_%Y") + '.log'
	directory = 'logs'
	f = open('/home/jefferson/Desktop/' + fname,'a')
	f.write('\n'+info)
