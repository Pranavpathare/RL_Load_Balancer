class Request:
    def _init_(self, method = 'NORM'):
        self.granted = False
        self._method = method
        
        if self._method == 'GET':
            self.size = np.random.randint(1, 5)
        elif self._method == 'POST':
            self.size = np.random.randint(3, 10)
        elif self._method == 'NORM':
            self.size = 4
        else:
            #print("No such method")
            self.size = 4
            self._method = 'NORM'
            
        self.src_ip = '.'.join(tuple(map(str,np.random.randint(0, 255, 4))))
        
    def _del_(self):
        #print("Request Complete .. Being deleted.")
        pass

    def _repr_(self):
        return f"Request('{self._method}')"

    def _str_(self):
        return f"Request Object\nMethod: {self._method}\nSize: {self.size}\nGranted: {self.granted}"