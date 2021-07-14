# This page to check the nginx config for proxying websockets
from dazzler.system import Page
from dazzler.components import core


page = Page(
    __name__,
    core.Container([
        core.Input(identity='input'),
        core.Container(identity='output')
    ]),
    url='/deep/nested/url'
)


@page.bind('value@input')
async def on_value(ctx):
    await ctx.set_aspect('output', children=ctx.trigger.value)

