from __future__ import annotations as _annotations

from fastapi import APIRouter
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.events import GoToEvent


def sidebar_menu(*components: AnyComponent, title: str | None = None) -> list[AnyComponent]:
    return [
        c.PageTitle(text=f"FastUI Demo — {title}" if title else "FastUI Demo"),
        c.Navbar(
            title="FastUI Demo",
            title_event=GoToEvent(url="/"),
            start_links=[
                c.Link(
                    components=[c.Text(text="Components")],
                    on_click=GoToEvent(url="/components"),
                    active="startswith:/components",
                ),
                c.Link(
                    components=[c.Text(text="Tables")],
                    on_click=GoToEvent(url="/table/cities"),
                    active="startswith:/table",
                ),
                c.Link(
                    components=[c.Text(text="Auth")],
                    on_click=GoToEvent(url="/auth/login/password"),
                    active="startswith:/auth",
                ),
                c.Link(
                    components=[c.Text(text="Forms")],
                    on_click=GoToEvent(url="/forms/login"),
                    active="startswith:/forms",
                ),
            ],
        ),
        c.Page(
            components=[
                *((c.Heading(text=title),) if title else ()),
                *components,
            ],
        ),
        c.Footer(
            extra_text="FastUI Demo",
            links=[
                c.Link(
                    components=[c.Text(text="Github")], on_click=GoToEvent(url="https://github.com/pydantic/FastUI")
                ),
                c.Link(components=[c.Text(text="PyPI")], on_click=GoToEvent(url="https://pypi.org/project/fastui/")),
                c.Link(components=[c.Text(text="NPM")], on_click=GoToEvent(url="https://www.npmjs.com/org/pydantic/")),
            ],
        ),
    ]


router = APIRouter()


@router.get("/", response_model=FastUI, response_model_exclude_none=True)
def api_index() -> list[AnyComponent]:
    # language=markdown
    markdown = """\
This site provides a demo of [FastUI](https://github.com/pydantic/FastUI), the code for the demo
is [here](https://github.com/pydantic/FastUI/tree/main/demo).

You can find the documentation for FastUI [here](https://docs.pydantic.dev/fastui/).

HERE SHOULD BE THE MAIN CONTENT

HERE ARE POSSIBLE FORM FACTORS:
* `Markdown` — that's me :-)
* `Text`— example [here](/components#text)
* `Paragraph` — example [here](/components#paragraph)
* `PageTitle` — you'll see the title in the browser tab change when you navigate through the site
* `Heading` — example [here](/components#heading)
* `Code` — example [here](/components#code)
* `Button` — example [here](/components#button-and-modal)
* `Link` — example [here](/components#link-list)
* `LinkList` — example [here](/components#link-list)
* `Navbar` — see the top of this page
* `Footer` — see the bottom of this page
* `Modal` — static example [here](/components#button-and-modal), dynamic content example [here](/components#dynamic-modal)
* `ServerLoad` — see [dynamic modal example](/components#dynamic-modal) and [SSE example](/components#server-load-sse)
* `Image` - example [here](/components#image)
* `Iframe` - example [here](/components#iframe)
* `Video` - example [here](/components#video)
* `Toast` - example [here](/components#toast)
* `Table` — See [cities table](/table/cities) and [users table](/table/users)
* `Pagination` — See the bottom of the [cities table](/table/cities)
* `ModelForm` — See [forms](/forms/login)

Authentication is supported via:
* token based authentication — see [here](/auth/login/password) for an example of password authentication
* GitHub OAuth — see [here](/auth/login/github) for an example of GitHub OAuth login
"""
    return sidebar_menu(c.Markdown(text=markdown))


@router.get("/{path:path}", status_code=404)
async def api_404():
    # so we don't fall through to the index page
    return {"message": "Not Found"}
