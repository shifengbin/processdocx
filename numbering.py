from idmanager import generate_id


class Numbering:
    def __init__(self, numbering=None):
        self.numbering = numbering

    def generate_id(self, suffix):
        if not self.numbering:
            return
        abstract_nums = self.numbering.find_all("abstractNum")
        for abstract_num in abstract_nums:
            abstract_num["w:abstractNumId"] = generate_id(abstract_num["w:abstractNumId"], suffix, "")

        nums = self.numbering.find_all("num")
        for num in nums:
            num["w:numId"] = generate_id(num["w:numId"], suffix, "")

        abstract_num_ids = self.numbering.find_all("abstractNumId")
        for abstract_num_id in abstract_num_ids:
            abstract_num_id["w:val"] = generate_id(abstract_num_id["w:val"], suffix, "")

    def get_dom(self):
        return self.numbering

    def get_numbering(self):
        if not self.numbering:
            return []
        return self.numbering.find("numbering").children

    def merge(self, numbering):
        if not self.numbering:
            self.numbering = numbering.get_dom()
            return
        numberings = self.numbering.find("numbering")
        for num in numbering.get_numbering():
            numberings.append(num)










