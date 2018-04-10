from uuid import uuid1


class IdAble:
    def __init__(self):
        self.id = uuid1().hex

'''
class IdManager:
    id_cache = dict()

    def generate_id(self, obj):
        return self.id_cache.setdefault(obj.id, uuid1().hex)
'''


def generate_id(sid, suffix):
    if not sid:
        return None
    s_ids = sid.split("_")
    to_id = s_ids[0] + "_" + suffix
    return to_id
