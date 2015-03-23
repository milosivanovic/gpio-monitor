#!/usr/bin/python

import os
import select

class GPIO(object):

	GPIO_EXPORT = "/sys/class/gpio/export"
	GPIO_UNEXPORT = "/sys/class/gpio/unexport"

	GPIO_TEMPLATE_DIRECTION = "/sys/class/gpio/gpio%d/direction"
	GPIO_TEMPLATE_EDGE = "/sys/class/gpio/gpio%d/edge"
	GPIO_TEMPLATE_VALUE = "/sys/class/gpio/gpio%d/value"

	def __init__(self, ports):
		self.ports = ports
		self.fds = {}

		for name, port in self.ports.iteritems():
			try:
				self.unexport(port)
			except IOError:
				pass
			self.export(port)
			self.set_direction(port, 'in')
			self.set_trigger(port, 'both')
			self.fds[name] = None

	def monitor(self):
		self.loop()

	def unexport(self, port):
		with open(GPIO.GPIO_UNEXPORT, 'w') as file:
			file.write("%s\n" % port)
			file.close()

	def export(self, port):
		with open(GPIO.GPIO_EXPORT, 'w') as file:
			file.write("%s\n" % port)
			file.close()

	def set_direction(self, port, direction):
		with open(GPIO.GPIO_TEMPLATE_DIRECTION % port, 'w') as file:
			file.write("%s\n" % direction)
			file.close()

	def set_trigger(self, port, edge):
		with open(GPIO.GPIO_TEMPLATE_EDGE % port, 'w') as file:
			file.write("%s\n" % edge)
			file.close()

	def get_value(self, port):
		with open(GPIO.GPIO_TEMPLATE_VALUE % port) as file:
			file.read()
			file.close()

	def loop(self):
		epoll = select.epoll()
		for name, port in self.ports.iteritems():
			self.fds[name] = open(GPIO.GPIO_TEMPLATE_VALUE % port, 'r')
			epoll.register(self.fds[name], select.EPOLLIN | select.EPOLLET)

		n = 0

		while True:
			n += 1
			events = epoll.poll()

			if n == 1:
				# skip the first iteration, because all that
				# does is tell us the current value of the port
				continue

			for fileno, event in events:
				for name, file in self.fds.iteritems():
					if fileno == file.fileno():
						# seek to the beginning of the file because that's
						# how the Linux kernel presents overwritten GPIO information
						file.seek(0)

						result = int(file.read().strip())
						self.parse(name, result)

	def parse(self, name, status):
		if name == "AC_OK":
			print "AC_OK STATUS: %d" % status
		elif name == "BAT_OK":
			print "BAT_OK STATUS: %d" % status

if __name__ == '__main__':
	gpio = GPIO({
		'AC_OK': 199,
		'BAT_OK': 200
	})
	gpio.monitor()
