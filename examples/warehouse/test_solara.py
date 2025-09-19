import solara

@solara.component
def Page():
    solara.Markdown("# Hello Solara!")

# Create a simple test page
page = Page()