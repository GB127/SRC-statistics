from code_SRC.composantes import Time


class Test_time:
    def test_init(self):
        assert Time(4).__dict__ == {"seconds":4}

    def test_str(self):
        assert str(Time(500000)) == "138:53:20"


    def test_operators(self):
        assert Time(1) == Time(1)
        assert Time(1) + Time(2) == Time(3)
        assert Time(3) - Time(2) == Time(1)
        assert Time(1) <= Time(2)
        assert Time(1) < Time(2)
        assert Time(2) / 2 == Time(1)
        assert Time(10) / Time(2) == 10/2
        assert float(Time(10)) == 10.0