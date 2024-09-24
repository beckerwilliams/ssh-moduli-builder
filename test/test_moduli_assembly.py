from pathlib import PosixPath as Path
from unittest import TestCase
from uuid import uuid4 as uuid

from moduli_assembly.__main__ import (default_config, generate_candidates, get_moduli_dir, get_screened_path,
                                      screen_candidates)
from moduli_assembly.config_manager.config_manager import (ConfigManager)


def create_faux_moduli(application_config_dir) -> None:
    screening_dir = Path.home().joinpath(application_config_dir, ".moduli")
    screening_dir.mkdir(exist_ok=True, parents=True)
    for i in range(29):
        screening_dir.joinpath(f"{uuid()}").touch()


def harvest_artifacts(conf):
    """
    Vampire Function | Harvest Generated Candidate Files for Async Screening Tests
    :param conf:
    :type conf:
    :return:
    :rtype:
    """
    resource_dir = Path("test/moduli_dir")
    for file in Path.joinpath(conf["config_dir"], ".moduli").glob("????.*"):
        resource_dir.joinpath(file.name).write_bytes(file.read_bytes())


def load_test_artifacts(config):
    """
    We Harvest Candidate Files from test_generate_candidates,
    and use them HERE, TRUNCATED for Faster Processing
    :param config:
    :type config:
    :return:
    :rtype:
    """
    resource_dir = Path("test/moduli_dir")
    if not get_moduli_dir(config).exists():
        get_moduli_dir(config).mkdir(exist_ok=True, parents=True)

    for file in resource_dir.glob("????.candidate*"):
        get_moduli_dir(config).joinpath(file.name).touch()
        # We'll use just 3000 Moduli Lines from Candidate File to enable
        saved_lines = file.read_text().splitlines()[:3000]
        # Write truncated Candidate File
        get_moduli_dir(config).joinpath(file.name).write_text('\n'.join(saved_lines))


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
    def test_generate_and_screen_candidates(cls) -> None:
        """
        generate ONE batch of Moduli Candidate Files, Verify Existence
        :return:
        :rtype:
        """
        # generate ONE batch of Moduli Candidate Files
        if not get_moduli_dir(cls.cm.config).exists():
            get_moduli_dir(cls.cm.config).mkdir(exist_ok=True, parents=True)
        candidate_file = generate_candidates(2048, 1, cls.cm.config)
        cls.assertTrue(cls, candidate_file.stat().st_size > 2048)
        candidate_files = [file for file in
                           (Path.home().joinpath(cls.cm.config["config_dir"], '.moduli')).glob('????.candidate*')]
        cls.assertTrue(len(candidate_files) > 0, "No Moduli Candidate Files")
        # Let's Reuse some of our work ;-}
        harvest_artifacts(cls.cm.config)

    def test_screen_candidates(cls) -> None:
        # Test Screen Candidate File - first in Glob/Indeterminate
        load_test_artifacts(cls.cm.config)
        candidate_file = [file for file in
                          (Path.home().joinpath(cls.cm.config["config_dir"], '.moduli'))
                          .glob('????.candidate*')][0]
        screen_candidates(candidate_file, cls.cm.config)
        cls.assertTrue(cls, get_screened_path(candidate_file, cls.cm.config).stat().st_size > 2048)
        screened_files = [file for file in
                          get_moduli_dir(cls.cm.config).glob('????.screened*')]
        cls.assertTrue(len(screened_files) > 0, "No Moduli Candidate Files")

        # Vampire Function
        try:
            harvest_artifacts(cls.cm.config)
        except Exception() as err:
            print(err)
