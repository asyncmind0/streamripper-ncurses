import subprocess

class Player:
    _process = None
    @classmethod
    def start(cls):
        if cls._process:
            cls.stop()
        cls._process = subprocess.Popen([
            'mplayer', 
            'http://localhost:8000' ], 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)

    @classmethod
    def stop(cls):
        if cls._process:
            cls._process.terminate()
            cls._process.wait()

    @classmethod
    def pause(cls):
        if cls._process:
            cls._process.stdin.write(' ')
            
    @classmethod
    def volup(cls):
        if cls._process:
            cls._process.stdin.write('*')
            
    @classmethod
    def voldown(cls):
        if cls._process:
            cls._process.stdin.write('/')
