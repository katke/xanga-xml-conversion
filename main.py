#!/usr/bin/env python3

import datetime
import sys
import xml.etree.ElementTree as elementTree

# <rss version="2.0"
# xmlns:excerpt="http://wordpress.org/export/1.1/excerpt/"
# xmlns:content="http://purl.org/rss/1.0/modules/content/"
# xmlns:wfw="http://wellformedweb.org/CommentAPI/"
# xmlns:dc="http://purl.org/dc/elements/1.1/"
# xmlns:wp="http://wordpress.org/export/1.1/">

# IDS_NS   =  "http://whatever/the/IDS/namespace/value/is" #adjust this to the real IDS NS
# ET.register_namespace("IDS", IDS_NS)
# et.SubElement(root, et.QName(IDS_NS, "OwnedPropertyRentNetCust"))

# for filename in sys.argv[1:]:
def parse_file(xmlFile):
    # for filename in xmlFile:
    tree = elementTree.parse(xmlFile)
    root = tree.getroot()
    namespaces = {
        "content": "http://purl.org/rss/1.0/modules/content/",
        "wp": "http://wordpress.org/export/1.1/"
    }
    result = ""
    # elementTree.register_namespace("content", CONTENT_NS)
    for item in root.findall(".//item"):
        title = item.find("title").text
        if title is None:
            title = "No title"
        blog_post = item.find("content:encoded", namespaces).text
        comment_section = item.find("wp:comment", namespaces)
        comments = comment_section.findall("wp:comment_content", namespaces)
        dateString = item.find("pubDate").text
        dateStringWithoutColon = dateString[:-3] + dateString[-2:]
        date = datetime.datetime.strptime(dateStringWithoutColon, "%a, %d %b %Y %H:%M:%S %z")
        htmlTemplateString = "<h3>{0}</h3><div>{1}</div>\n"
        result += htmlTemplateString.format(date, blog_post)
    with open("html_xanga.html", "w") as f:
        f.write(result)
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parse_file('./xanga_archives_copy/2592092_4.xml')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
