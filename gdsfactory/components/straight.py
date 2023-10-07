"""Straight waveguide."""
from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.cross_section import CrossSectionSpec


@gf.cell
def straight(
    length: float = 10.0,
    npoints: int = 2,
    layer: gf.typings.LayerSpec | None = None,
    width: float | None = None,
    add_pins: bool = True,
    cross_section: CrossSectionSpec = "xs_sc",
) -> Component:
    """Returns a Straight waveguide.

    Args:
        length: straight length (um).
        npoints: number of points.
        layer: layer to use. Defaults to cross_section.layer.
        width: width to use. Defaults to cross_section.width.
        add_pins: add pins to the component.
        cross_section: specification (CrossSection, string or dict).

    .. code::

        o1 -------------- o2
                length
    """
    p = gf.path.straight(length=length, npoints=npoints)
    x = gf.get_cross_section(cross_section)

    if layer or width:
        x = x.copy(layer=layer or x.layer, width=width or x.width)

    c = Component()
    path = p.extrude(x)
    ref = c << path
    c.add_ports(ref.ports)

    x.add_bbox(c, right=0, left=0)
    if add_pins:
        x.add_pins(c)
    c.info["length"] = length
    c.info["width"] = x.sections[0].width
    c.add_route_info(cross_section=x, length=length)
    c.absorb(ref)
    return c


if __name__ == "__main__":
    import klayout.db as kdb

    import gdsfactory as gf

    # c = gf.Component()
    # ref = c << straight(cross_section="xs_rc")
    # ref2 = c << straight(cross_section="xs_rc")
    # ref2.center = ref.center + kdb.Point(0, 1000)
    # ref2.d.move((0, 10))
    # ref.name = "straight"
    # print(c.insts['straight'].ports)
    c = straight(cross_section="xs_rc")
    c.show()
