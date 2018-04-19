from idmanager import generate_id, generate_file_name
from template import get_image_relationship_dom


class Relationships:
    def __init__(self, relationships):
        self.relationships = relationships
        self.file_mapping = None
        self.start_id = 100

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
            rs["Id"] = generate_id(rs["Id"], suffix)
            source = rs['Target']
            temp_target = generate_file_name(source, suffix)
            rs['Target'] = temp_target
            self.file_mapping[source] = temp_target

    def append_relationship(self, suffix):
        rid = "rId" + str(self.start_id)
        filename = "image" + str(self.start_id) + "." +suffix
        self.start_id += 1
        dom = get_image_relationship_dom(rid, filename)
        self.relationships.find("Relationships").append(dom)
        return {"rid": rid, "filename": filename}



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



