from template import get_png_contenttype, get_jpg_contenttype


class ContentTypes:
    def __init__(self, content):
        self.content = content
        self.types = None
        self.extension = {}

    def get_dom(self):
        return self.content

    def get_types_dom(self):
        types = []
        for type_ in self.content.find("Types").children:
            if "Extension" in type_:
                self.extension[type_["Extension"]] = True
            if "header" not in type_["ContentType"] and "footer" not in type_["ContentType"]:
                types.append(type_)

        #print(types)
        return types

    def get_types(self):
        if self.types:
            return self.types
        types = list()
        for child in self.get_types_dom():
            content_type = child['ContentType']
            if content_type not in types:
                types.append(content_type)
        self.types = types
        return types

    def merge_content_types(self, content):
        if not isinstance(content, ContentTypes):
            raise Exception("parameter is not ContentTypes")
        types_dom = self.content.find("Types")
        types = self.get_types()
        for child in content.get_types_dom():
            content_type = child["ContentType"]
            if content_type in types:
                continue
            types_dom.append(child)

    def append_png(self):
        if "png" in self.extension:
            return
        self.extension["png"] = True
        self.content.find("Types").insert(0, get_png_contenttype())

    def append_jpeg(self):
        if "jpg" in self.extension:
            return
        self.extension["jpg"] = True
        self.content.find("Types").insert(0, get_jpg_contenttype())

    def append_extension(self, suffix):
        suffix = suffix.lower()
        if suffix == "png":
            self.append_png()
        else:
            self.append_jpeg()
