import subprocess

class Ripper:
    def __init__(self,url):
        self._url = url

    def start(self):
        self._process = subprocess.Popen([
            'streamripper', 
            self._url, 
            '-r'
            ])

    def stop(self):
        if self._process:
            self._process.terminate()
            self._process.wait()

_ripper = None

def start(url):
    global _ripper
    if not _ripper:
        _ripper = Ripper(url)
        _ripper.start()

def stop():
    global _ripper
    if _ripper:
        _ripper.stop()
