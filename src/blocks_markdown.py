def markdown_to_blocks(markdown):
    return list(map(
        lambda md: md.strip(),
        markdown.split("\n\n"))
    )
