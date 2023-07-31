from diffractGUI.Transform import Rotation, RotationList


def test_one_rotation():
    rotations = RotationList()

    rotations.add(Rotation(name="X", axis_of_rotation=(1.0, 0.0, 0.0)))
    #rotations.add(rotation about y by -0.1)
    #rotations.add(rotation about y by 0.1)
    #rotations.add(rotation about z by 0.1)

    assert len(rotations) == 1
    for rotation in rotations:
        assert rotation.angle_of_rotation == 0.0


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
