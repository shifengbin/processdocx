from bs4 import BeautifulSoup
from zipfile import ZipFile
from uuid import uuid1
import os
from PIL import Image

from idmanager import IdAble
from document import Document
from contenttypes import ContentTypes
from relationships import Relationships
from styles import Styles
from numbering import Numbering


TEMP_BASE_DIR = os.path.join("/tmp", "docxs_temp")


class Docx(IdAble):
    def __init__(self, path):
        super(Docx, self).__init__()
        if path is None or not isinstance(path,str):
            raise Exception("Path is not allowed None")
        if not os.path.exists(TEMP_BASE_DIR):
            try:
                os.mkdir(TEMP_BASE_DIR)
            except FileExistsError as e:
                pass
        self.document = None
        self.content_types = None
        self.relationships = None
        self.numbering = None
        self.styles = None
        self.base_dir = uuid1().hex
        file = ZipFile(path)
        self.file_path = os.path.join(TEMP_BASE_DIR, self.base_dir)
        os.mkdir(self.file_path)
        file.extractall(self.file_path)
        file.close()
        self.get_document()
        self.get_content_types()
        self.get_numbering()
        self.get_relationships()
        self.get_styles()

    def get_numbering(self):
        if self.numbering:
            return self.numbering
        numbering_path = os.path.join(self.file_path, "word/numbering.xml")
        if not os.path.exists(numbering_path):
            self.numbering = Numbering()
            return self.numbering
        with open(numbering_path, encoding="UTF-8") as f:
            numbering = f.read()
        numbering = BeautifulSoup(numbering, "xml")
        self.numbering = Numbering(numbering)
        return self.numbering

    def get_document(self):
        if self.document:
            return self.document
        doc_path = os.path.join(self.file_path, "word/document.xml")
        with open(doc_path, encoding="UTF-8") as f:
            document = f.read()
        document = BeautifulSoup(document, "xml")
        self.document = Document(document)
        return self.document

    def get_relationships(self):
        if self.relationships:
            return self.relationships
        doc_path = os.path.join(self.file_path, "word/_rels/document.xml.rels")
        with open(doc_path, encoding="UTF-8") as f:
            doc = f.read()
        doc = BeautifulSoup(doc, "xml")
        self.relationships = Relationships(doc)
        return self.relationships

    def get_content_types(self):
        if self.content_types:
            return self.content_types
        content_path = os.path.join(self.file_path, "[Content_Types].xml")
        with open(content_path, encoding="UTF-8") as f:
            content_types = f.read()
            content_types = BeautifulSoup(content_types, "xml")
        self.content_types = ContentTypes(content_types)
        return self.content_types

    def get_styles(self):
        if self.styles:
            return self.styles
        style_path = os.path.join(self.file_path, "word/styles.xml")
        with open(style_path, encoding="UTF-8") as f:
            styles = f.read()

        styles = BeautifulSoup(styles, "xml")
        self.styles = Styles(styles)
        return self.styles

    def extract_media_files(self, path):
        relationships = self.get_relationships()
        file_mapping = relationships.get_file_mapping()
        template = "cp {} {}"

        base_dir = os.path.join(self.file_path, "word")
        #print(file_mapping)
        for file in file_mapping.keys():
            from_file = os.path.join(base_dir, file)
            to_file = os.path.join(path, file_mapping[file])

            dir_name = os.path.dirname(to_file)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            extract = template.format(from_file, to_file)
            os.system(extract)

    def merge(self, doc, page=False):
        if not isinstance(doc, Docx):
            raise Exception("merge parameter is not docx")
        source_content_types = doc.get_content_types()
        self.get_content_types().merge_content_types(source_content_types)

        source_relationships = doc.get_relationships()
        #print(source_relationships.get_file_mapping())
        source_relationships.generate_id(doc.id)
        doc.extract_media_files(os.path.join(self.file_path, "word"))
        self.get_relationships().merge_relationships(source_relationships)

        source_styles = doc.get_styles()
        source_styles.generate_id(doc.id)
        self.styles.merge(source_styles)

        source_numberings = doc.get_numbering()
        source_numberings.generate_id(doc.num)
        self.numbering.merge(source_numberings)

        source_document = doc.get_document()
        source_document.generate_id(doc.id, doc.num)
        self.get_document().merge(source_document, page)

    def save(self, name):
        import zipfile

        self._save_document()
        self._save_content_types()
        self._save_relationships()
        self._save_numbering()
        self._save_styles()

        file = ZipFile(name, "w", compression=zipfile.ZIP_DEFLATED)
        for base, children, files in os.walk(self.file_path):
            base_name = base.split(self.base_dir)[-1]
            for f in files:
                zip_path = os.path.join(base_name, f)
                real_path = os.path.join(base, f)
                file.write(real_path, zip_path)
        file.close()

    def _save_document(self):
        with open(os.path.join(self.file_path,"word/document.xml"), mode="w", encoding="UTF-8") as f:
            f.write(str(self.document.get_dom()))

    def _save_content_types(self):
        with open(os.path.join(self.file_path, "[Content_Types].xml"), mode="w", encoding="UTF-8") as f:
            f.write(str(self.content_types.get_dom()))

    def _save_relationships(self):
        with open(os.path.join(self.file_path, "word/_rels/document.xml.rels"), mode="w", encoding="UTF-8") as f:
            f.write(str(self.relationships.get_dom()))

    def _save_numbering(self):
        numbering = self.numbering.get_dom()
        if not numbering:
            return
        numbering_path = os.path.join(self.file_path, "word/numbering.xml")
        with open(numbering_path, "w+", encoding="UTF-8") as f:
            f.write(str(numbering))

    def _save_styles(self):
        with open(os.path.join(self.file_path, "word/styles.xml"), "w+", encoding="UTF-8") as f:
            f.write(str(self.styles.get_dom()))

    def append_paragraph(self, text, align="left"):
        self.document.append_paragraph(text, align)

    def append_picture(self, filepath, align="left"):
        if not os.path.exists(filepath):
            return
        media_dir = os.path.join(self.file_path, "word/media")
        if not os.path.exists(media_dir):
            os.mkdir(media_dir)
        suffix = filepath.split(".")[-1]
        self.content_types.append_extension(suffix)
        id_file = self.relationships.append_relationship(suffix)
        #print(id_file)
        file_path = os.path.join(self.file_path, "word/media/{filename}".format(filename=id_file["filename"]))
        os.system("cp {f_file} {t_file}".format(f_file=filepath, t_file=file_path))
        img = Image.open(file_path)
        width, height = img.size
        img.close()
        self.document.append_picture(id_file["rid"], width*6350, height*6350, align)

    def close(self):
        os.system("rm -rf {0}".format(self.file_path))


def merge_files(filespath, to_filename, page=False):
    if type(filespath) != list:
        raise Exception("filespath not list")
    merge_list = []
    index = 0
    for filename in filespath:
        if not os.path.exists(filename):
            continue
        docx = Docx(filename)
        #docx.id = str(index)
        index += 1
        merge_list.append(docx)
    root = merge_list[0]
    for docx in merge_list[1:]:
        root.merge(docx, page)
        docx.close()
    root.save(to_filename)
    root.close()


def make_new_document():
    template = os.path.join(os.path.dirname(__file__), "templates/template.docx")
    return Docx(template)

if __name__ == "__main__":
    '''
    doc = Docx("1.docx")

    document = doc.get_document()
    contents = document.get_content()
    count = 0
    for content in contents:
        document.clear_content()
        document.append_content(content.get_dom())
        doc.save("a/{}.docx".format(count))
        count += 1
    doc.close()
    '''
    #merge_files(["a/0.docx", "a/1.docx", "a/2.docx", "a/3.docx"], "bb.docx")
    #merge_files(["1.docx", "123456.docx", "654321.docx"], "bb.docx", True)
    #merge_files(["1.docx", "a.docx", "bbb.docx"], "bb.docx", True)
    #for x in range(2):
    #    merge_files(["1.docx", "123456.docx", "654321.docx", "bb.docx"], "bb.docx")
    #print(__file__)

    doc = make_new_document()
    doc.append_paragraph("aaaaa", "center")
    doc.append_paragraph("bbb", "left")
    doc.append_paragraph("ccc", "right")
    doc.append_picture("./1.png", "left")
    doc.append_picture("./1.png", "left")
    doc.append_picture("./2.png", "left")
    doc.append_picture("./2.png", "center")
    doc.append_paragraph("ddd", "right")
    doc.save("bbb.docx")
    doc.close()

