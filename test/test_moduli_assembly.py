from pathlib import PosixPath as Path
from unittest import TestCase
from uuid import uuid4 as uuid

from moduli_assembly.__main__ import (default_config, generate_candidates)
from moduli_assembly.config_manager.config_manager import (ConfigManager)


def create_faux_moduli(application_config_dir) -> None:
    screening_dir = Path.home().joinpath(application_config_dir, ".moduli")
    screening_dir.mkdir(exist_ok=True, parents=True)
    for i in range(29):
        screening_dir.joinpath(f"{uuid()}").touch()


# noinspection PyTypeChecker
class TestModuliAssemblyCore(TestCase):
    """
    Unittests of moduli_assembly.py functions

    """

    @classmethod
    def setUp(cls) -> None:
        # args = {
        #     "version": False,
        #     "clear_artifacts": False,
        #     "export_config": False,
        #     "write_moduli": False,
        #     "restart": False,
        #     "remove_config_dir": False,
        #     "all": [3072]
        # }
        # Load Configuration Manager with Application Defaults from moduli_assembly.__main__
        cls.cm = ConfigManager(default_config())
        cls.app_config = Path.home().joinpath('.moduli_assembly/.config').absolute()

        # create_faux_moduli(cls.cm.config['config_dir'])  # FOR TESTING Clear Artifacts

    @classmethod
    def tearDown(cls) -> None:
        pass
        # del cls.cm

    # @classmethod
    # def test_always_true_placeholder(cls):
    #     """
    #     Faux Test - Always Successful
    #     :return: True
    #     :rtype: bool
    #     """
    #     cls.assertTrue(cls, True)  # add assertion here

    @classmethod
    def test_application_config(cls) -> None:
        """
        Verify Application Operates with Application's Config Properties, not those of Config Manager

        :return:
        :rtype:
        """
        cls.assertCountEqual(cls, str(cls.cm.config["config_file"]), str(cls.app_config),
                             "Discrepancy Between Application and Config Manager Properties")

    @classmethod
    def test_generate_candidates(cls) -> None:
        """
        generate ONE batch of Moduli Candidate Files, Verify Existence
        :return:
        :rtype:
        """
        # generate ONE batch of Moduli Candidate Files
        candidate_file = generate_candidates(2048, 1, cls.cm.config)
        all_files = [file for file in (Path.home().joinpath(cls.cm.config["config_dir"], '.moduli')).glob('*')]
        cls.assertTrue(len(all_files) > 0, "No Moduli Candidate Files")
        cls.assertTrue(cls, candidate_file.exists())
        cls.assertTrue(cls, candidate_file.stat().st_size > 0)
        candidate_files = [file for file in cls.cm.config['config_dir'].joinpath('.moduli').glob('????.candidate*')]
        cls.assertTrue(len(candidate_files) > 0, "We should have at least ONE candidate file")

    # @classmethod
    # def test_clear_artifacts(cls) -> None:
    #     current_files = [file for file in (cls.cm.config['config_dir'].joinpath('.moduli')).glob('*')]
    #     cls.assertGreaterEqual(cls, len(current_files), 1, "No Files Found in .moduli_assembly/.moduli")
    #     clear_artifacts(cls.cm.config)
    #     current_files = [file for file in (cls.cm.config['config_dir'].joinpath('.moduli')).glob('*')]
    #     cls.assertLessEqual(cls, len(current_files), 0, "Failed to Delete All Files")
