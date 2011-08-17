import subprocess

class Player:
    def start(self):
        self._process = subprocess.Popen([
            'mplayer', 
            'http://localhost:8000' 
            ])

    def stop(self):
        if self._process:
            self._process.terminate()
            self._process.wait()

_player  = None

def start():
    global _player
    if not _player:
        _player = Player()
        _player.start()


def stop():
    global _player
    if _player:
        _player.stop()
