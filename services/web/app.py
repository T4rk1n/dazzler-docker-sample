import os
import sys

from dazzler import Dazzler
from dazzler.system import Page, BindingContext, transforms as t
from dazzler.components import core

sys.path.insert(0, '.')

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
    app.config.requirements.static_directory = '/home/app/web/assets'

    await app._on_parse(app.cli.parser.parse_args([]))
    app.logger.warn(f'backend {app.config.session.backend}')
    app.logger.warn(f'CWD: {os.getcwd()}')
    app.logger.info(f'LS: {os.listdir(os.getcwd())}')
    app.logger.info(f'CONFIG_PATH: {app.config_path}')
    return await app.application()

