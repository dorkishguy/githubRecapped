from api import main

from textual import on
from textual.containers import Center, Container, Middle
from textual.widgets import Input, Header, Label
from textual.app import App
from textual.containers import Grid

class Recapped(App):
    CSS_PATH = "styles.tcss"

    def on_mount(self):
        self.query_one("#stats", Grid).display = "none"
        self.title = "Github Recapped"
        self.sub_title = "A TUI frontend"

    def compose(self):
        yield Header()
        with Center():
            yield Input(placeholder="GitHub Username", id="a")
        with Grid(id="stats"):
            with Container(classes="stat"):
                yield Label(id="numberStarred")
            with Container(classes="stat"):
                yield Label(id="numberRepos")
            with Container(classes="stat"):
                yield Label(id="leastStars")
            with Container(classes="stat"):
                yield Label(id="maxStars")
            with Container(classes="stat"):
                yield Label(id="totalStars")
            with Container(classes="stat"):
                yield Label(id="age")
            with Container(classes="stat"):
                yield Label(id="mostStarred")
            with Container(classes="stat"):
                yield Label(id="lang")

    @on(Input.Submitted, "#a")
    def getUn(self, event: Input.Submitted):
        un = event.value
        event.input.display = "none"
        try:
            data = main(un)
            self.log(data)
        except Exception:
            self.log(Exception)
            self.notify("something went wrong", severity="error")
            event.input.styles.display = "block"
            event.input.value = ""
            event.input.focus()
            return
        self.query_one("#stats", Grid).display = True
        self.query_one("#numberStarred", Label).update(f"Number of repos starred: {data["numberStarred"]}")
        self.query_one("#numberRepos", Label).update(f"Number of repos: {data["numberRepos"]}")
        self.query_one("#leastStars", Label).update(f"Least stars: {data["leastStars"]}")
        self.query_one("#maxStars", Label).update(f"Max stars: {data["maxStars"]}")
        self.query_one("#totalStars", Label).update(f"Total stars: {data["totalStars"]}")
        self.query_one("#age", Label).update(f"Age: {data["age"]} days")
        self.query_one("#mostStarred", Label).update(f"Most starred: {data["mostStarred"]}")
        self.query_one("#lang", Label).update(f"Fav language: {data["lang"][0][0]}")

def main():
    app = Recapped()
    app.run()

if __name__ == "__main__":
    main()