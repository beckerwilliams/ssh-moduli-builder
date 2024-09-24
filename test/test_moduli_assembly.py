from pathlib import PosixPath as Path
from unittest import TestCase
from uuid import uuid4 as uuid

from moduli_assembly.__main__ import (default_config, generate_candidates, get_moduli_dir, get_screened_path,
                                      screen_candidates)
from moduli_assembly.config_manager.config_manager import (ConfigManager)


def create_faux_moduli(application_config_dir) -> None:
    screening_dir = Path.home().joinpath(application_config_dir, ".moduli")
    screening_dir.mkdir(exist_ok=True, parents=True)
    for _ in range(7):
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
    Unittests of ModuliAssembly.py functions

    """

    @classmethod
    def setUp(self) -> None:

        # Load Configuration Manager with Application Defaults from moduli_assembly.__main__
        self.cm = ConfigManager(default_config())
        self.app_config = Path.home().joinpath('.moduli_assembly/.config').absolute()

        # create_faux_moduli(self.cm.config['config_dir'])  # FOR TESTING Clear Artifacts

    @classmethod
    def tearDown(self) -> None:
        del self.cm

    @classmethod
    def test_application_config(self) -> None:
        """
        Verify Application Operates with Application's Config Properties, not those of Config Manager

        :return:
        :rtype:
        """
        self.assertCountEqual(self, str(self.cm.config["config_file"]), str(self.app_config),
                              "Discrepancy Between Application and Config Manager Properties")

    @classmethod
    def test_generate_candidates(self) -> None:
        """
        generate ONE batch of Moduli Candidate Files, Verify Existence
        :return:
        :rtype:
        """
        # generate ONE batch of Moduli Candidate Files
        if not get_moduli_dir(self.cm.config).exists():
            get_moduli_dir(self.cm.config).mkdir(exist_ok=True, parents=True)
        candidate_file = generate_candidates(2048, 1, self.cm.config)
        self.assertTrue(self, candidate_file.stat().st_size > 2048, "Candidate File Insufficient Entries")
        candidate_files = [file for file in
                           (Path.home().joinpath(self.cm.config["config_dir"], '.moduli')).glob('????.candidate*')]
        self.assertTrue(self, len(candidate_files) > 0, "No Moduli Candidate Files")
        # Let's Reuse some of our work ;-}
        harvest_artifacts(self.cm.config)

    @classmethod
    def test_screen_candidates(self) -> None:
        """
        Screen ONE Truncated Candidate File, Currently with only 3000 lines.
        :return:
        :rtype:
        """
        # Test Screen Candidate File - first in Glob/Indeterminate
        load_test_artifacts(self.cm.config)
        candidate_file = [file for file in
                          (self.cm.get_moduli_dir(self.cm.config))
                          .glob('????.candidate*')][0]
        screen_candidates(candidate_file, self.cm.config)
        self.assertTrue(self, get_screened_path(candidate_file, self.cm.config).stat().st_size > 0, "Empty File")
        screened_files = [file for file in
                          get_moduli_dir(self.cm.config).glob('????.screened*')]
        self.assertTrue(self, len(screened_files) > 0, "No Moduli Screening Files")

        # Vampire Function
        try:
            harvest_artifacts(self.cm.config)
        except Exception() as err:
            print(err)

# Launching unittests with arguments python -m unittest test.test_moduli_assembly in /Users/ron/development/ssh-moduli-builder
#
# Generating candidate files for modulus size: 2048
# Mon Sep 23 22:38:41 2024 Sieve next 67043328 plus 2047-bit
# Mon Sep 23 22:40:48 2024 Sieved with 203277289 small primes in 127 seconds
# Mon Sep 23 22:40:50 2024 Found 56564 candidates
# Screening /Users/ron/.moduli_assembly/.moduli/2048.candidate_2024-09-23T16:17:52.539204+00:00 for Safe Primes (generator=2)
# Mon Sep 23 22:40:57 2024 Found 1 safe primes of 1490 candidates in 7 seconds
# /Users/ron/.moduli_assembly/.moduli/2048.candidate_2024-09-23T16:17:52.539204+00:00 Unlinked
#
#
# Ran 3 tests in 136.129s
