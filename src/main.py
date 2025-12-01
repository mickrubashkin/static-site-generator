import sys
from build_content import copy_content, generate_page, generate_pages_recursive


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_content("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()
