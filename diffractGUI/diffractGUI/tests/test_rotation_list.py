import clifford

from diffractGUI.Transform import Rotation, RotationList


def test_one_rotation():
    rotations = RotationList()

    rotations.add(Rotation(name="X", axis_of_rotation=(1.0, 0.0, 0.0)))
    # rotations.add(rotation about y by -0.1)
    # rotations.add(rotation about y by 0.1)
    # rotations.add(rotation about z by 0.1)

    assert len(rotations) == 1
    for rotation in rotations:
        assert rotation.angle_of_rotation == 0.0

    rotor = rotations.rotor()
    # should leave any point unchanged
    _, blades = clifford.Cl(4)
    a_point = blades["e4"] + blades["e1"]
    print(f"a_point: {a_point}")
    a_rotated_point = rotor * a_point * ~rotor
    print(f"a rotated point: {a_rotated_point}")
    assert a_point == a_rotated_point


def test_combine_rotations():
    rotations = RotationList()

    rotation1 = Rotation(name="X", axis_of_rotation=(1.0, 0.0, 0.0))
    rotation1.angle_of_rotation = 1.0

    rotations.add(rotation1)

    rotation2 = Rotation(name="X", axis_of_rotation=(1.0, 0.0, 0.0))
    rotation2.angle_of_rotation = 1.0

    rotations.add(rotation2)

    assert len(rotations) == 1
    assert rotations[-1].axis_of_rotation == (1.0, 0.0, 0.0)
    assert rotations[-1].angle_of_rotation == 2.0


def test_one_rotation_rotor():
    rotations = RotationList()

    rotation1 = Rotation(name="X", axis_of_rotation=(1.0, 0.0, 0.0))
    rotation1.angle_of_rotation = 180.0

    rotations.add(rotation1)

    rotor = rotations.rotor()

    _, blades = clifford.Cl(4)
    a_point = blades["e4"] + blades["e2"]
    a_rotated_point = rotor * a_point * ~rotor
    expected_rotated_point = blades["e4"] - blades["e2"]
    print(f"a_rotated_point: {a_rotated_point}")
    print(f"expected_rotated_point: {expected_rotated_point}")
    assert a_rotated_point == expected_rotated_point

def test_two_rotation_rotor():
    rotations = RotationList()

    rotation1 = Rotation(name="X", axis_of_rotation=(1.0, 0.0, 0.0), angle_of_rotation=90.0)
    rotations.add(rotation1)

    rotation2 = Rotation(name="Z", axis_of_rotation=(0.0, 0.0, 1.0), angle_of_rotation=90.0)
    rotations.add(rotation2)

    rotor = rotations.rotor()

    _, blades = clifford.Cl(4)
    a_point = blades["e4"] + blades["e2"]
    a_rotated_point = rotor * a_point * ~rotor
    expected_rotated_point = blades["e4"] + blades["e3"]
    print(f"a_rotated_point: {a_rotated_point}")
    print(f"expected_rotated_point: {expected_rotated_point}")
    assert a_rotated_point == expected_rotated_point
