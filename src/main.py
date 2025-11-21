from textnode import TextNode, TextType


print("hello world")

def main():
    dummy_text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(dummy_text_node)

main()
