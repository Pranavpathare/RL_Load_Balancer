
import numpy as np
from collections import deque
import time
import threading

from client import Client
from client import Request

# ## Final ALBQueue

class ALBQueue(deque):
    def __init__(self):
        super()
    
    def queue_length(self):
        """Current len of queue"""
        return len(self)
    
    def time_exp(self):
        """Time Taken to service Requests proportional to this"""
        return sum([item.size for item in self])
    
    def post_count(self):
        """Count of POST method Requests in Queue"""
        return sum([item._method == 'POST' for item in self])
    
    def get_count(self):
        """Count of GET method Requests in Queue"""
        return sum([item._method == 'GET' for item in self])
