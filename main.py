#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as elementTree

XML_NAMESPACES = {
        "content": "http://purl.org/rss/1.0/modules/content/",
        "wp": "http://wordpress.org/export/1.1/",
        "dc": "http://purl.org/dc/elements/1.1/",
        "wfw": "http://wellformedweb.org/CommentAPI/",
        "excerpt": "http://wordpress.org/export/1.1/excerpt/"
    }

def parse_file(xml_file):
    tree = elementTree.parse(xml_file)
    root = tree.getroot()
    result = ""
    for item in root.findall(".//item"):
        blog_post = item.find("content:encoded", XML_NAMESPACES).text
        comment_section = item.findall("wp:comment", XML_NAMESPACES)
        comment_markup = generate_comments(comment_section)
        wrapped_comment_markup = "<div class=\"comments-section\"><h2>Comments</h2>{0}</div>".format(comment_markup)
        dateString = item.find("wp:post_date", XML_NAMESPACES).text
        htmlTemplateString = "<div class=\"post\"><h2 class=\"post-date\">{0}</h2><div class=\"post-content\">{1}</div>{2}</div>"
        result += htmlTemplateString.format(dateString, blog_post, wrapped_comment_markup)
    return result

def generate_comments(comments):
    comment_markup = ""
    if len(comments) > 0:
        for comment in comments:
            comment_content = comment.find("wp:comment_content", XML_NAMESPACES).text
            comment_content_markup = "<div class=\"content\">{0}</div>".format(comment_content)
            comment_date = comment.find("wp:comment_date", XML_NAMESPACES).text
            comment_author = comment.find("wp:comment_author", XML_NAMESPACES).text
            comment_author_url = comment.find("wp:comment_author_url", XML_NAMESPACES).text
            comment_author_markup = "<p><a href=\"{0}\">{1}</a> wrote:</p>".format(comment_author_url, comment_author)
            comment_markup_template = "<div class=\"comment\"><p>{0}</p>{1}{2}</div>"
            comment_markup += comment_markup_template.format(
                comment_date,
                comment_author_markup,
                comment_content_markup)
    else:
        comment_markup = "<p>No comments to display.</p>"
    return comment_markup

if __name__ == '__main__':
    archive_file_names = sys.argv[1:]
    html_markup = "<link rel=\"stylesheet\" href=\"./styles.css\" />"
    for xml_file in archive_file_names:
        parsed_file_markup = parse_file(xml_file)
        html_markup += parsed_file_markup
    with open("html_xanga.html", "w") as f:
        f.write(html_markup)
