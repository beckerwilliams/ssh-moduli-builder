from json import loads
from pathlib import PosixPath as Path
from unittest import TestCase

from moduli_assembly.config_manager.config_manager import ConfigManager, default_config


# noinspection PyTypeChecker
class TestConfigManager(TestCase):

    # Setup - Start Each Test with CLEAN Config Directory
    @classmethod
    def setUp(cls) -> None:
        cls.defaultCM = ConfigManager()

        cls.user_conf = {"config_dir": "ConfigManagerTestDir", "config_file": "cm_conf",
                         "application_property_0": "application_value_0",
                         "application_property_1": "application_value_1",
                         "application_property_N": "application_value_N"}
        cls.userCM = ConfigManager(cls.user_conf)

    @classmethod
    def tearDown(cls) -> None:
        for test_config in [default_config(), cls.user_conf]:
            if Path.home().joinpath(test_config["config_dir"], test_config["config_file"]).exists():
                Path.home().joinpath(test_config["config_dir"], test_config["config_file"]).unlink()
                Path.home().joinpath(test_config["config_dir"]).rmdir()

    #
    @classmethod
    def test__init__(cls) -> None:
        # cls.assertIsInstance(cls, cls.defaultCM, ConfigManager)
        cls.assertIsInstance(cls, cls.userCM, ConfigManager)

    @classmethod  #
    def test_config_type(cls) -> None:
        # cls.assertIsInstance(cls, cls.defaultCM.config, dict)
        cls.assertIsInstance(cls, cls.userCM.config, dict)

    @classmethod  #
    def test_config_required_properties(cls) -> None:
        cls.assertIn(cls, 'config_dir', cls.defaultCM.config)
        cls.assertIn(cls, 'config_file', cls.defaultCM.config)
        cls.assertIn(cls, 'config_dir', cls.userCM.config)
        cls.assertIn(cls, 'config_file', cls.userCM.config)

    #
    @classmethod  #
    def test_config_required_values_not_none(cls) -> None:
        cls.assertIsNotNone(cls, cls.defaultCM.config['config_dir'])
        cls.assertIsNotNone(cls, cls.defaultCM.config['config_file'])
        cls.assertIsNotNone(cls, cls.userCM.config['config_dir'])
        cls.assertIsNotNone(cls, cls.userCM.config['config_file'])

    #
    @classmethod
    def test_config_file_creation(cls) -> None:
        cls.assertTrue(cls, cls.defaultCM.config['config_file'].exists())
        cls.assertTrue(cls, cls.userCM.config['config_file'].exists())

        for conf_file in [cls.userCM.config['config_file'], cls.defaultCM.config['config_file']]:
            user_config = loads(conf_file.read_text())
            cls.assertIn(cls, 'config_dir', user_config)
            cls.assertIn(cls, 'config_file', user_config)
            cls.assertIsInstance(cls, user_config['config_dir'], str)
            cls.assertIsInstance(cls, user_config['config_file'], str)
