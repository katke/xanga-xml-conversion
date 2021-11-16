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

def parse_file(xml_file):
    tree = elementTree.parse(xml_file)
    root = tree.getroot()
    namespaces = {
        "content": "http://purl.org/rss/1.0/modules/content/",
        "wp": "http://wordpress.org/export/1.1/"
    }
    result = ""
    for item in root.findall(".//item"):
        blog_post = item.find("content:encoded", namespaces).text
        comment_section = item.findall("wp:comment", namespaces)
        comment_markup = ""
        if len(comment_section) > 0:
            for comment in comment_section:
                comment_content = comment.find("wp:comment_content", namespaces).text
                comment_content_markup = "<div class=\"content\">{0}</div>".format(comment_content)
                comment_date = comment.find("wp:comment_date", namespaces).text
                comment_author = comment.find("wp:comment_author", namespaces).text
                comment_author_url = comment.find("wp:comment_author_url", namespaces).text
                comment_author_markup = "<p><a href=\"{0}\">{1}</a> wrote:</p>".format(comment_author_url, comment_author)
                comment_markup_template = "<div class=\"comment\"><p>{0}</p>{1}{2}</div>"
                comment_markup += comment_markup_template.format(comment_date, comment_author_markup, comment_content_markup)
        else:
            comment_markup = "<p>No comments to display.</p>"
        wrapped_comment_markup = "<div class=\"comments-section\"><h2>Comments</h2>{0}</div>".format(comment_markup)
        dateString = item.find("wp:post_date", namespaces).text
        htmlTemplateString = "<div class=\"post\"><h2 class=\"post-date\">{0}</h2><div class=\"post-content\">{1}</div>{2}</div>"
        result += htmlTemplateString.format(dateString, blog_post, wrapped_comment_markup)
    return result


if __name__ == '__main__':
    archive_file_names = sys.argv[1:]
    html_markup = "<link rel=\"stylesheet\" href=\"./styles.css\" />"
    for xml_file in archive_file_names:
        parsed_file_markup = parse_file(xml_file)
        html_markup += parsed_file_markup
    with open("html_xanga.html", "w") as f:
        f.write(html_markup)

