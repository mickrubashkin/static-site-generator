from build_content import copy_content, generate_page, generate_pages_recursively


print("hello world")

def main():
    copy_content("static", "public")
    generate_pages_recursively("content", "template.html", "public")

main()
