# App from dazzler readme.
from dazzler import Dazzler
from dazzler.system import Page, BindingContext, transforms as t
from dazzler.components import core

app = Dazzler(__name__)
page = Page(
    __name__,
    core.Container([
        core.Html('H2', 'My dazzler page'),
        core.Container('Please enter a name', identity='visitor-name'),
        core.Input(value='', identity='input'),
        core.Button('Save name', identity='save-btn', disabled=True),
    ], identity='layout', id='layout'),
    title='My Page',
    url='/'
)

# UI updates via tie & transforms
page.tie('value@input', 'disabled@save-btn').transform(
    t.Length().t(t.Lesser(1))
)


# Bindings executes on the server via websockets.
@page.bind('clicks@save-btn')
async def on_click(context: BindingContext):
    # Save the visitor name via session system
    name = await context.get_aspect('input', 'value')
    await context.session.set('visitor', name)
    await context.set_aspect(
        'visitor-name', children=f'Saved {name}'
    )


# Aspects defined on the layout trigger on initial render and
# allows to insert initial data.
@page.bind('id@layout')
async def on_layout(context: BindingContext):
    visitor = await context.session.get('visitor')
    if visitor:
        await context.set_aspect(
            'visitor-name', children=f'Welcome back {visitor}!'
        )


app.add_page(page)


async def app_factory():
    # Set the static directory only for deployment.
    app.config.requirements.static_directory = '/home/app/web/assets'
    return await app.application()

