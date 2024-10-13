#!/usr/bin/env python 3
from pathlib import PosixPath as Path
from unittest import TestCase

from moduli_assembly import (ModuliAssembly, __version__, default_config)


def _load_candidate(target_moduli_dir: Path = None) -> Path:
    """
    Copies earliest Candidate File found in 'test/resources' to working moduli directory, .moduli_assembly/.moduli
    :return: None
    :rtype:
    """
    if not target_moduli_dir:
        target_moduli_dir = Path.home().joinpath('.moduli_assembly', '.moduli')

    # Resource File MAINTENANCE - Lets keep the LAST 8 Candidates produced - delete the remaining
    candidates = [file for file in Path('test/resources').glob('????.candidate*')]
    if len(candidates) > 7:
        # We'll keep 7 versions of Candidate File around - refreshed every test
        archive_candidates = candidates[0:(len(candidates) - 7)]
        for candidate in archive_candidates:
            candidate.unlink()
        # Refresh List after Elimination of List Elements
        candidates = [file for file in Path('test/resources').glob('????.candidate*')]

    # Grab First Avaialble Canidate File
    candidate = candidates[0]

    # Copy contents of RESOURCE file to RUNTIME file
    target_moduli_dir.joinpath(candidate.name).write_text(candidate.read_text())

    # Create 'In-Progress' Checkpoint File for Screening Operations
    # - We use 50000 as the STARTING line in the Modulus File, which gives about 6000 to screen. [OPTIMIZATION]
    target_moduli_dir.joinpath(f'.{candidate.name}').write_text('50000\n')
    return target_moduli_dir.joinpath(candidate.name)


def _store_candidate(candidate_file: Path) -> None:
    Path('test/resources').joinpath(candidate_file.name).write_text(candidate_file.read_text())


class TestModuliAssembly(TestCase):

    def setUp(cls):
        cls.ma = ModuliAssembly()
        cls.config_dir = Path.home().joinpath('.moduli_assembly')
        cls.moduli_dir = cls.ma.config['moduli_dir']
        cls.test_version = __version__

    def tearDown(cls):
        pass

    def test_ModuliAssembly_default_config(cls):
        cls.assertTrue(cls, cls.ma.config is not None)
        for attr in default_config():
            cls.assertTrue(cls, attr in cls.ma.config)
            cls.assertTrue(cls, 'generator_type' in cls.ma.config)
            cls.assertTrue(cls, 'auth_key_lengths' in cls.ma.config)
            cls.assertTrue(cls, 'config_file' in cls.ma.config)
            cls.assertTrue(cls, 'config_dir' in cls.ma.config)
            cls.assertTrue(cls, 'moduli_dir' in cls.ma.config)

    def test_ModuliAssembly_missing_attrs(cls):
        for attr in default_config():
            with cls.assertRaises(AttributeError) as exception:
                config = default_config()
                del config[attr]
                ModuliAssembly(config)
            print(f'Success: Exception Tested: {exception.exception}')

    def test_get_moduli_dir(cls):
        cls.assertEqual(cls.ma.config['moduli_dir'], cls.moduli_dir)

    def test_create_candidate_path(cls):
        # Vars for get_candidate_file
        key_length = 2048
        tpath = str(cls.ma.config['moduli_dir'].joinpath(f'{key_length}.candidate_'))
        cls.assertTrue(tpath in str(cls.ma.create_candidate_path(key_length)))

    # def test_get_screened_path(cls):
    #     key_length = 2048
    #     cp = cls.ma.create_candidate_path(key_length)
    #     # Get screened path, convert to candidate and compare to given candidate file
    #     cls.assertTrue(str(cp.parent.joinpath(cls.ma.get_screened_path(cp)))
    #                    .replace('screened', 'candidate') == str(cp.absolute()))

    # def test_generate_candidates(cls):
    #     """
    #     Generate Candidate Moduli Files via ssh-keygen -M generate ...
    #     :return: None
    #     :rtype: None
    #     """
    #     candidate_file = cls.ma.generate_candidates(2048, 1)
    #     cls.assertTrue(candidate_file.exists())
    #     cls.assertTrue(candidate_file.stat().st_size > 1)
    #     cls.assertTrue(len(candidate_file.read_text().split('\n')) > 50000)
    #
    #     # Preserve Candidate for Screening Run
    #     Path('test/resources').joinpath(candidate_file.name).write_text(candidate_file.read_text())
    #
    # def test_screen_candidates(cls):
    #     # Copy Pre-Generated Candidates to Moduli Dir for Screen Testing
    #     candidate_file = _load_candidate(cls.ma.config['moduli_dir'])
    #     screened_file = cls.ma.screen_candidates(candidate_file)
    #
    #     cls.assertTrue(screened_file.exists())
    #     cls.assertTrue(screened_file.stat().st_size > 1)
    #     cls.assertTrue(len(screened_file.read_text().split('\n')) > 1)
    #
    # def test_restart_candidate_screening(cls):
    #     candidate_file = _load_candidate(cls.ma.config['moduli_dir'])
    #     cls.ma.restart_candidate_screening()
    #     cls.assertTrue(cls.ma.get_screened_path(candidate_file).exists())
    #     cls.assertTrue(cls.ma.get_screened_path(candidate_file).stat().st_size > 1)
    #     cls.assertTrue(len(cls.ma.get_screened_path(candidate_file).read_text().split('\n')) > 1)

    # def test_write_moduli_file(cls):
    #     moduli_file = cls.ma.write_moduli_file()
    #     cls.assertTrue(moduli_file.exists())
    #     cls.assertTrue(moduli_file.stat().st_size > 1)
    #
    # def test_write_named_moduli_file(cls):
    #     moduli_file = cls.ma.write_moduli_file(cls.ma.config['config_dir'].joinpath('TEST_MODULI_FILE'))
    #     cls.assertTrue(moduli_file.exists())
    #     cls.assertTrue(moduli_file.stat().st_size > 1)
    #
    # def test_get_version(cls):
    #     cls.assertTrue(cls.ma.version == __version__)
    #
    # def test_config(cls):
    #     pass
