import numpy as np

from diffractGUI.AtomicPlanes import AtomicPlanes

def test_init():
    atomic_planes = AtomicPlanes()

    # expect 26 atomic planes
    assert len(atomic_planes.atomic_planes) == 26

    # no rotation has been applied yet
    for plane_info in atomic_planes.atomic_planes.values():
        assert plane_info["plane"] == plane_info["rotated_plane"]
        assert plane_info["normal"] == plane_info["rotated_normal"]


def test_angles_with_planes():
    atomic_planes = AtomicPlanes()

    angles_with_planes = atomic_planes.angles_with_planes(a_line=(1.0, 0.0, 0.0))

    assert len(angles_with_planes) == 26
    assert np.isclose(angles_with_planes["-(1.0^e124) - (1.0^e234)"]["angle"], np.deg2rad(45.0))
 