from uuid import uuid1
import random

class IdAble:
    def __init__(self):
        self.id = uuid1().hex
        self.num = random.randint(100, 60000)


def generate_id(sid, suffix, separation="_"):
    if not sid:
        return None
    '''
    s_ids = sid.split("_")
    to_id = s_ids[0] + "_" + suffix
    '''
    to_id = str(sid) + separation + str(suffix)
    return to_id


def generate_file_name(fname, suffix):
    if not fname:
        return None
    fnames = fname.split(".")
    temp_name = fnames[0]+"_"+suffix+"."+fnames[-1]
    return temp_name
