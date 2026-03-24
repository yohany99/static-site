from textnode import TextType, TextNode
from gencontent import generate_pages_recursive, copy_static

def main():
    copy_static("./static", "./public")
    generate_pages_recursive("./content", "./template.html", "./public")

if __name__ == "__main__":
    main()