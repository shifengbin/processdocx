from idmanager import generate_id


class Relationships:
    def __init__(self, relationships):
        self.relationships = relationships
        self.file_mapping = None

    def get_relationships(self):
        return [child for child in self.relationships.find("Relationships").children
                if child['Target'].startswith("media")
                or child['Target'].startswith("embeddings")]

    def get_dom(self):
        return self.relationships

    def merge_relationships(self, relationships):
        if not isinstance(relationships, Relationships):
            raise Exception("parameter is not Relationships")

        root = self.relationships.find("Relationships")

        rs = relationships.get_relationships()

        for r in rs:
            root.append(r)

    def get_file_mapping(self):
        if self.file_mapping:
            return self.file_mapping
        rs = self.get_relationships()
        file_mapping = dict()

        for r in rs:
            file_mapping[r["Target"]] = r["Target"]
        self.file_mapping = file_mapping
        return file_mapping

    def generate_id(self, suffix):
        if not self.file_mapping:
            self.file_mapping = dict()

        for rs in self.get_relationships():
            #temp_id = rs["Id"].split("_")
            #temp_id = temp_id[0]+"_"+suffix
            #rs["Id"] = temp_id
            rs["Id"] = generate_id(rs["Id"], suffix)

            temp_target = rs['Target'].split("_")
            if len(temp_target) > 1:
                temp_target = temp_target[0] + "_" + suffix + "." + temp_target[1].split(".")[-1]
            else:
                temp = temp_target[0].split(".")
                temp_target = temp[0] + "_" + suffix + "." + temp[-1]
            rs['Target'] = temp_target
            temp_name = temp_target.split("_"+suffix)
            self.file_mapping[temp_name[0]+temp_name[-1]] = temp_target


if __name__ == "__main__":
    from bs4 import BeautifulSoup
    with open("a/document.xml.rels" ,encoding="UTF-8") as f:
        data = f.read()
    soup = BeautifulSoup(data, "xml")
    relationships = Relationships(soup)
    rs = relationships.get_relationships()
    for r in rs:
        print(r)
    print("--------------------", relationships.get_file_mapping())
    relationships.generate_id("12")
    for r in rs:
        print(r)
    print("--------------------", relationships.get_file_mapping())
    relationships.generate_id("23")
    for r in rs:
        print(r)
    print("--------------------", relationships.get_file_mapping())



