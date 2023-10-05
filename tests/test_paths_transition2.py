from __future__ import annotations

import gdsfactory as gf


def test_transition_ports() -> None:
    width1 = 0.5
    width2 = 1.0
    x1 = gf.cross_section.strip(width=width1)
    x2 = gf.cross_section.strip(width=width2)
    xt = gf.path.transition(cross_section1=x1, cross_section2=x2, width_type="linear")
    path = gf.path.straight(length=5)
    c = gf.path.extrude_transition(path, xt)
    assert c.ports["o1"].width == width1, c.ports["o1"].width
    assert c.ports["o2"].width == width2, c.ports["o2"].width
    assert c.ports["o1"].cross_section.width == width1, c.ports[
        "o1"
    ].cross_section.width
    assert c.ports["o2"].cross_section.width == width2, c.ports[
        "o2"
    ].cross_section.width


if __name__ == "__main__":
    # test_transition_ports()

    width1 = 0.5
    width2 = 1.0
    x1 = gf.cross_section.strip(width=0.5)
    x2 = gf.cross_section.strip(width=1.0)

    xt = gf.path.transition(cross_section1=x1, cross_section2=x2, width_type="linear")
    path = gf.path.straight(length=5)
    c = gf.path.extrude_transition(path, xt)
    assert c.ports["o1"].width == width1, c.ports["o1"].width
    assert c.ports["o2"].width == width2, c.ports["o2"].width
    assert c.ports["o1"].cross_section.width == width1, c.ports[
        "o1"
    ].cross_section.width
    assert c.ports["o2"].cross_section.width == width2, c.ports[
        "o2"
    ].cross_section.width
    c.show()
