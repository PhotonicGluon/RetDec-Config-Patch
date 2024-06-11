# IMPORTS
import os
import tempfile

from retdec_config_patch.config import Config


# TESTS
class TestConfig:
    empty_config = Config()
    fake_config = Config()
    fake_config.retdec_binary = "fake1"

    def test_repr(self):
        assert repr(self.empty_config) == "<RetDec Configuration>"
        assert repr(self.fake_config) == "<RetDec Configuration>"

    def test_str(self):
        assert str(self.empty_config) == "{'retdec_binary': None}"
        assert str(self.fake_config) == "{'retdec_binary': 'fake1'}"

    def test_serialize(self):
        assert self.empty_config._serialize() == {"retdec_binary": None}
        assert self.fake_config._serialize() == {"retdec_binary": "fake1"}

    def test_deserialize(self):
        test_config_1 = Config()
        test_config_1._deserialize({"attr1": 1, "attr2": False})
        assert test_config_1.attr1 == 1
        assert not test_config_1.attr2
        assert test_config_1.retdec_binary is None

        test_config_2 = Config()
        test_config_2._deserialize({"attr3": 1, "retdec_binary": "fake", "attr4": False})
        assert test_config_2.attr3 == 1
        assert not test_config_2.attr4
        assert test_config_2.retdec_binary == "fake"

    def test_is_empty(self):
        assert self.empty_config.is_empty()
        assert not self.fake_config.is_empty()

    def test_io(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path = os.path.join(tempdir, "test-config.json")

            config = Config.load(path)
            assert config.is_empty()

            config.retdec_binary = "fake"
            config.save(path)
            assert os.path.exists(path)

            config = Config.load(path)
            assert not config.is_empty()
            assert config.retdec_binary == "fake"

            Config.remove(path)
            assert not os.path.exists(path)
