import os
import subprocess

class Ripper:
    _process = None

    @classmethod
    def start(cls,url, directory='ripped'):
        if not os.path.isdir(directory):
            os.mkdir(directory)
        cls._process = subprocess.Popen([
            'streamripper', 
            url, 
            '-r',
            '-d', 'ripped'],
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)

    @classmethod
    def stop(cls):
        if cls._process:
            cls._process.terminate()
            cls._process.wait()

