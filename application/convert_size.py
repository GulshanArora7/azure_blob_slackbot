import math

class SIZE_CONVERSION:
    def __init__(self, size_bytes ):
        self.size_bytes = size_bytes

    def convert_size(self): 
        if self.size_bytes == 0: 
            return "0B" 
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB") 
        i = int(math.floor(math.log(self.size_bytes, 1024)))
        power = math.pow(1024, i) 
        size = round(self.size_bytes / power, 2) 
        return "{} {}".format(size, size_name[i])