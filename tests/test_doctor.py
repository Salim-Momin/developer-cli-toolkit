from devkit.commands.doctor import doctor


def test_doctor_runs():

    result = doctor()

    assert result is None
