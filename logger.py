import time

class Logger:
    def __init__(self,level="DEBUG") -> None:
        print(f'Logger init level <{level}>')
        self.level=level
        super().__init__()

    def get_time_tuple(self):
        _, _, _, hour, minute, second, _, _ = time.localtime()
        return (f"{hour}:{minute}:{second} >",)

    def set_level(self,level):
        self.level=level
        self.info(f"Set logger level <{level}>")


    def print(self, *args):
        print(*args)
        
    def error(self, *args):
        print(*(("[ERROR]:",)
        print(*(("[ERROR]:",)+self.get_time_tuple()+args))
        print(*(("[ERROR]:",)
        
    def info(self, *args):
        print(*(("[INFO ]:",)+self.get_time_tuple()+args))
        
    def debug(self, *args):
        if self.level=="DEBUG":
            print(*(("[DEBUG]",)+self.get_time_tuple()+args))
            
        
_logger = Logger()

def get_logger():
    return _logger

