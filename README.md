Python GPIO Monitor
====================

About
------
This is a generic GPIO monitor that doesn't depend on any specific platform, like Raspberry Pi, ODROID, Beagleboard, and so on.

How it works
-------------
It uses epoll() to give you interrupt-driven results; instant, and cheap on the CPU.
Currently only reading from GPIO ports is possible, but triggered write support will be added shortly.

How to use it
--------------
Simply specify which ports you would like to monitor, and you're away.

        gpio = GPIO({
                'LED1': 100,
                'LED2': 101
        })
        gpio.monitor()
