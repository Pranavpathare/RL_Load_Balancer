#!/usr/bin/env python
# coding: utf-8

import numpy as np
import time
from collections import deque
import threading

# 1. We are ignoring Caching here
# 2. Only One EXTRA Thread for Client Function used

# Final Request

class Request:
    """Request Object of method: GET POST CONST RAND\n"""
    def __init__(self, method = 'RAND'):
        self.granted = False
        self._method = method
        self.size = None
        
        if self._method == 'GET':
            self.size = np.random.randint(1, 5)
            
        elif self._method == 'POST':
            self.size = np.random.randint(3, 10)
            
        elif self._method == 'CONST':
            self.size = 4
            
        elif self._method == 'RAND':
            self._method = np.random.choice(('GET', 'POST'))
            self.__init__(self._method)
            
        self.src_ip = '.'.join(tuple(map(str,np.random.randint(0, 255, 4))))
        
    def __del__(self):
        #print("Request Complete .. Being deleted.")
        pass

    def __repr__(self):
        return f"Request('{self._method}')"

    def __str__(self):
        return f"Request Object\nMethod: {self._method}\nSize: {self.size}\nGranted: {self.granted}"


# ## Final Client

class Client:
    """Fires Requests towards the Load Balancer"""
    def __init__(self, deq):
        self._flag = 0
        self._deq = deq
        self._current = None
    
    def _uniform(self, r_type, rps : int): 
        """Uniformly fires Requests of type rtype"""
        sleep_duration = 1 / rps
        while self._flag == 2:
            new_r = Request(r_type)
            #print("U")
            self._deq.appendleft(new_r)
            time.sleep(sleep_duration*0.99)
    
    def _random(self, r_type, rps : int):
        """Fires Requests Randomly of type rtype : On average equals rps"""
        sleep_duration = 1 / rps
        while self._flag == 1:
            fill = min(2*sleep_duration, abs(0.5 * np.random.randn() + sleep_duration))
            #print("R")
            new_r = Request(r_type)
            self._deq.appendleft(new_r)
            time.sleep(fill)
    
    def _single(self, r_type):
        """Fires Single Request of type rtype"""
        new_r = Request(r_type)
        self._deq.appendleft(new_r)
        
    def _fire(self, method, r_type, rps):
        if method == 'stop':
            self._flag = 0
            if self._current:
                self._current.join()
            self._current = None

        elif method == 'uniform':
            self._flag = -1
            if self._current:
                self._current.join()
            self._flag = 2
            self._current = threading.Thread(target = self._uniform, args = (r_type, rps))
            self._current.start()
                
        elif method == "random":
            self._flag = -1
            if self._current:
                self._current.join()
            self._flag = 1
            self._current = threading.Thread(target = self._random, args = (r_type, rps))
            self._current.start()
            
        elif method == 'single':
            self._flag = -1
            if self._current:
                self._current.join()
            self._flag = 3
            self._current = None
            self._single(r_type) # Need thread here ?

    def fire(self, method, rtype = "RAND", rps = 5):
        """method: Type of firing -> 'uniform', 'random', 'single'\n
        rtype: 'RAND', 'GET', 'POST', 'CONST'\n\tdefault RAND\n
        rps: int\n\tdefault 5""" 
        self._fire(method, rtype, rps)
        
    def __str__(self):
        return f"Client Simulator for Deque"
