from bs4 import BeautifulSoup
import os


text_template = '<root xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">\
                <w:p><w:pPr><w:jc w:val="{align}"/></w:pPr><w:r><w:t>{text}</w:t></w:r></w:p></root>'


def get_text_dom(text, align="left"):
    text = text_template.format(text=text, align=align)
    soup = BeautifulSoup(text,"xml")
    return soup.find("p")

relationship_template = '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\
<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" \
Target="media/{filename}"/>\
</Relationships>'


def get_image_relationship_dom(rid, filename):
    template = relationship_template.format(rid=rid, filename=filename)
    soup = BeautifulSoup(template, "xml")
    return soup.find("Relationship")

image_template = '<root xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" \
xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" \
xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" \
xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" \
xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" \
xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">\
<w:p>\
<w:pPr>\
<w:jc w:val="{align}"/>\
<w:rPr>\
<w:rFonts w:ascii="Xingkai TC Light" w:eastAsia="Xingkai TC Light" w:hAnsi="Xingkai TC Light" w:hint="eastAsia"/>\
</w:rPr>\
</w:pPr>\
<w:r>\
<w:rPr>\
<w:rFonts w:ascii="Xingkai TC Light" w:eastAsia="Xingkai TC Light" w:hAnsi="Xingkai TC Light"/>\
<w:noProof/>\
</w:rPr>\
<w:drawing>\
<wp:inline>\
<wp:extent cx="{width}" cy="{height}"/>\
<wp:effectExtent l="0" t="0" r="0" b="0"/>\
<wp:docPr id="1" name="图片 1"/>\
<wp:cNvGraphicFramePr>\
<a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>\
</wp:cNvGraphicFramePr>\
<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">\
<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">\
<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">\
<pic:nvPicPr>\
<pic:cNvPr id="1" name=""/>\
<pic:cNvPicPr/>\
</pic:nvPicPr>\
<pic:blipFill>\
<a:blip r:embed="{rid}"/>\
<a:stretch>\
<a:fillRect/>\
</a:stretch>\
</pic:blipFill>\
<pic:spPr>\
<a:xfrm>\
<a:off x="0" y="0"/>\
<a:ext cx="{width}" cy="{height}"/>\
</a:xfrm>\
<a:prstGeom prst="rect">\
<a:avLst/>\
</a:prstGeom>\
</pic:spPr>\
</pic:pic>\
</a:graphicData>\
</a:graphic>\
</wp:inline>\
</w:drawing>\
</w:r>\
</w:p>\
</root>'


def get_image_dom(rid, width, height, align="left"):
    image = image_template.format(rid=rid, width=width, height=height, align=align)
    soup = BeautifulSoup(image, "xml")
    graphic = soup.find("graphic")
    graphic["xmlns:a"] = "http://schemas.openxmlformats.org/drawingml/2006/main"
    pic = soup.find("pic")
    pic["xmlns:pic"] = "http://schemas.openxmlformats.org/drawingml/2006/picture"
    gfl = soup.find("graphicFrameLocks")
    gfl["xmlns:a"] = "http://schemas.openxmlformats.org/drawingml/2006/main"
    return soup.find("p")


content_template_png = '<Default Extension="png" ContentType="image/png"/>'


def get_png_contenttype():
    soup = BeautifulSoup(content_template_png, "xml")
    return soup.find("Default")


content_template_jpg = '<Default Extension="jpg" ContentType="image/jpeg"/>'


def get_jpg_contenttype():
    soup = BeautifulSoup(content_template_jpg, "xml")
    return soup.find("Default")


document = os.path.join(os.path.dirname(__file__),"templates/document.xml")
with open(document, encoding="UTF-8") as f:
    document = f.read()


def get_image_dom2(rid, width, height, align="left"):
    soup = BeautifulSoup(document, "xml")
    print(soup.p.prettify())
    jc = soup.find("jc")
    jc["w:val"] = align

    extent = soup.find("extent")
    extent["cx"] = width
    extent["cy"] = height

    blip = soup.find("blip")
    blip["r:embed"] = rid
    return soup.p

if __name__ == "__main__":
    #dom = get_image_dom(123, 123,123)
    #print(dom.prettify())
    dom = get_image_dom2(123, 123,123)
    print(dom.prettify())
    #dom = get_image_relationship_dom("rid","filename")
    #print(dom.prettify())
    #dom = get_png_contenttype()
    #print(dom)



