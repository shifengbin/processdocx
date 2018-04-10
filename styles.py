from idmanager import generate_id


class Styles:
    def __init__(self, styles):
        self.styles = styles

    def get_styles(self):
        styles = self.styles.find_all("style")
        return styles

    def get_dom(self):
        return self.styles

    def generate_id(self, suffix):
        styles = self.get_styles()
        for style in styles:
            style["w:styleId"] = generate_id(style["w:styleId"], suffix)
            base = style.find("basedOn")
            if base:
                base["w:val"] = generate_id(base["w:val"], suffix)
            next_ = style.find("next")
            if next_:
                next_["w:val"] = generate_id(next_["w:val"], suffix)
            link = style.find("link")
            if link:
                link["w:val"] = generate_id(link["w:val"], suffix)

    def merge(self, styles):
        styles_source = styles.get_styles()
        styles_self = self.styles.find("styles")
        for style in styles_source:
            styles_self.append(style)




