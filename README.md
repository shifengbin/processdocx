# processdocx
### processdocx 是一个处理docx文件的库
##主要功能

1 文档拆分

> 可以按段落拆分,也可以提取文字
 
```
from docx import Docx
if __name__ == "__main__":
    doc = Docx("1.docx")

    document = doc.get_document()
    contents = document.get_content() #获取文档内容
    count = 0
    for content in contents:
        document.clear_content() #清空文档
        document.append_content(content.get_dom()) #添加想要的内容
        doc.save("a/{}.docx".format(count)) #保存文档
        count += 1
    doc.close() #关闭文档,清理临时文件
```
2 文档合并

> 可以一次合并多个文档,每个文档可以独立成页,也可以直接合并
 
```
from docxlib.docx import merge_files
if __name__ == "__main__":
  merge_files(["1.docx", "2.docx", "3.docx", "a.docx"], "bb.docx", True)
  #第一个参数是文档路径列表, 第二个是合并后保存文件的路径, 第三个参数是合并时是否分页,不填默认False
```

3 创建新文档

> 可以添加文字,图片,选择居左居右居中

