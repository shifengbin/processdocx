from bs4 import BeautifulSoup
from idmanager import generate_id

PAGE_TAG = BeautifulSoup('<root xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:p><w:r><w:br w:type="page"/></w:r></w:p></root>', 'xml')
PAGE_TAG = PAGE_TAG.find("p")

class Paragraph:
    def __init__(self, dom):
        self.dom = dom

    def get_content(self):
        return [t.text for t in self.dom.find_all("t")]

    def get_dom(self):
        return self.dom


class Document:
    def __init__(self, document):
        if not isinstance(document, BeautifulSoup):
            raise Exception("document is not BeautifulSoup")
        self.document = document

    def get_namespace(self):
        document = self.document.find("document")
        return document.attrs

    def merge_namespace(self, doc):
        if not isinstance(doc, Document):
            raise Exception("parameter is not Document")
        self.get_namespace().update(doc.get_namespace())

    def get_content(self):
        return [Paragraph(child) for child in self.document.find("body").children if not child.name.startswith("sectPr")]

    def clear_content(self):
        return self.document.find("body").clear()

    def append_content(self, dom):
        self.document.find("body").append(dom)

    def get_dom(self):
        return self.document

    def generate_style_id(self, suffix):
        pstyles = self.document.find_all("pStyle")
        for style in pstyles:
            style["w:val"] = generate_id(style["w:val"], suffix)

    def generate_media_id(self, suffix):
        medias = self.document.find_all("blip")
        for media in medias:
            media["r:embed"] = generate_id(media["r:embed"], suffix)

    def generate_object_id(self, suffix):
        objs = self.document.find_all("imagedata")
        for obj in objs:
            obj["r:id"] = generate_id(obj["r:id"], suffix)
        oles = self.document.find_all("OLEObject")
        for ole in oles:
            ole["r:id"] = generate_id(ole["r:id"], suffix)

    def generate_id(self, suffix):
        self.generate_style_id(suffix)
        self.generate_media_id(suffix)
        self.generate_object_id(suffix)

    def merge(self, document, page=False):
        self.document.attrs.update(document.get_dom().attrs)
        source_content = document.get_content()
        self_content = self.get_content()
        section = self.document.find("sectPr").extract()
        body = self.document.find("body")
        body.clear()
        for s_content in self_content:
            body.append(s_content.get_dom())
        if page:
            body.append(PAGE_TAG)
        for src_content in source_content:
            body.append(src_content.get_dom())
        body.append(section)

