class ContentTypes:
    def __init__(self, content):
        self.content = content
        self.types = None

    def get_dom(self):
        return self.content

    def get_types_dom(self):
        types = [types for types in self.content.find("Types").children
                if "header" not in types["ContentType"]
                and "footer" not in types["ContentType"]]
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
