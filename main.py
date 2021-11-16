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


# for filename in sys.argv[1:]:
def parse_file(xmlFile):
    # for filename in xmlFile:
    tree = elementTree.parse(xmlFile)
    root = tree.getroot()
    namespaces = {
        "content": "http://purl.org/rss/1.0/modules/content/",
        "wp": "http://wordpress.org/export/1.1/"
    }
    result = "<link rel=\"stylesheet\" href=\"./styles.css\" />"
    for item in root.findall(".//item"):
        title = item.find("title").text
        if title is None:
            title = "No title"
        blog_post = item.find("content:encoded", namespaces).text
        comment_section = item.findall("wp:comment", namespaces)
        comment_markup = ""
        if len(comment_section) > 0:
            for comment in comment_section:
                comment_content = comment.find("wp:comment_content", namespaces).text
                comment_date = comment.find("wp:comment_date", namespaces).text
                comment_author = comment.find("wp:comment_author", namespaces).text
                comment_author_url = comment.find("wp:comment_author_url", namespaces).text
                comment_markup_template = "<div class=\"comment\"><p>{0}</p><a href=\"{1}\">{2}</a> wrote:<div class=\"content\">{3}</div></div>"
                comment_markup += comment_markup_template.format(comment_date, comment_author_url, comment_author, comment_content)
        else:
            comment_markup = "<p>No comments to display.</p>"
        wrapped_comment_markup = "<div class=\"comments-section\"><h2>Comments</h2>{0}</div>".format(comment_markup)
        dateString = item.find("pubDate").text
        dateStringWithoutColon = dateString[:-3] + dateString[-2:]
        date = datetime.datetime.strptime(dateStringWithoutColon, "%a, %d %b %Y %H:%M:%S %z")
        htmlTemplateString = "<div class=\"post\"><h1 class=\"post-title\">{0}</h1><h4 class=\"post-date\">{1}</h4><div class=\"post-content\">{2}</div>{3}</div>"
        result += htmlTemplateString.format(title, date, blog_post, wrapped_comment_markup)
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
