from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.straight import straight as straight_function
from gdsfactory.components.taper import taper as taper_function
from gdsfactory.typings import ComponentFactory, CrossSectionSpec


@gf.cell
def mmi2x2(
    width: float | None = None,
    width_taper: float = 1.0,
    length_taper: float = 10.0,
    length_mmi: float = 5.5,
    width_mmi: float = 2.5,
    gap_mmi: float = 0.25,
    taper: ComponentFactory = taper_function,
    straight: ComponentFactory = straight_function,
    with_bbox: bool = True,
    cross_section: CrossSectionSpec = "xs_sc",
    **kwargs,
) -> Component:
    r"""Mmi 2x2.

    Args:
        width: input and output straight width.
        width_taper: interface between input straights and mmi region.
        length_taper: into the mmi region.
        length_mmi: in x direction.
        width_mmi: in y direction.
        gap_mmi: (width_taper + gap between tapered wg)/2.
        taper: taper function.
        straight: straight function.
        with_bbox: add rectangular box in cross_section
            bbox_layers and bbox_offsets to avoid DRC sharp edges.
        cross_section: spec.
        kwargs: cross_section settings.


    .. code::

                   length_mmi
                    <------>
                    ________
                   |        |
                __/          \__
            o2  __            __  o3
                  \          /_ _ _ _
                  |         | _ _ _ _| gap_mmi
                __/          \__
            o1  __            __  o4
                  \          /
                   |________|

                 <->
            length_taper

    """
    c = gf.Component()
    gap_mmi = gf.snap.snap_to_grid(gap_mmi, grid_factor=2)
    w_taper = width_taper
    x = gf.get_cross_section(cross_section, **kwargs)
    xs_mmi = x.copy(width=width_mmi)
    width = width or x.width

    _taper = taper(
        length=length_taper,
        width1=width,
        width2=w_taper,
        cross_section=x,
        add_pins=False,
    )

    a = gap_mmi / 2 + width_taper / 2
    mmi = c << straight(length=length_mmi, cross_section=xs_mmi, add_pins=False)

    ports = [
        gf.Port("o1", orientation=180, center=(0, -a), width=w_taper, cross_section=x),
        gf.Port("o2", orientation=180, center=(0, +a), width=w_taper, cross_section=x),
        gf.Port(
            "o3",
            orientation=0,
            center=(length_mmi, +a),
            width=w_taper,
            cross_section=x,
        ),
        gf.Port(
            "o4",
            orientation=0,
            center=(length_mmi, -a),
            width=w_taper,
            cross_section=x,
        ),
    ]

    for port in ports:
        taper_ref = c << _taper
        taper_ref.connect(port="o2", destination=port)
        c.add_port(name=port.name, port=taper_ref.ports["o1"])
        c.absorb(taper_ref)

    c.absorb(mmi)
    if with_bbox:
        x.add_bbox(c)
    if x.add_pins:
        x.add_pins(c)
    return c


if __name__ == "__main__":
    # c = mmi2x2(gap_mmi=0.252, cross_section="xs_m1")
    c = mmi2x2(gap_mmi=0.252)
    c.show()
    c.pprint()
