#!/usr/bin/env python 3
from pathlib import PosixPath as Path
from unittest import TestCase

from moduli_assembly.ModuliAssembly import (ModuliAssembly, default_config)


def _delete_fs(path: Path):
    if path.exists() and path.is_dir():
        for file in path.iterdir():
            if file.is_file() or file.is_symlink():
                file.unlink()
            else:
                _delete_fs(file)
    path.rmdir()


def _load_candidate() -> Path:
    """
    Copies earliest Candidate File found in 'test/resources' to working moduli directory, .moduli_assembly/.moduli
    :return: None
    :rtype:
    """

    candidate = [file for file in Path('test/resources').glob('????.candidate*')][0]
    mdir = Path.home().joinpath('.moduli_assembly/.moduli')
    mdir.joinpath(candidate.name).write_text(candidate.read_text())
    return mdir.joinpath(candidate.name)


def _store_candidate(candidate_file: Path) -> None:
    Path('test/resources').joinpath(candidate_file.name).write_text(candidate_file.read_text())


class TestModuliAssembly(TestCase):

    def setUp(cls):
        cls.ma = ModuliAssembly()
        cls.config_dir = Path.home().joinpath('.moduli_assembly')
        cls.moduli_dir = Path.home().joinpath('.moduli_assembly', '.moduli')
        cls.test_version = '0.10.1'

    def tearDown(cls):
        config_dir = Path.home().joinpath(cls.ma.config['config_dir'])
        if config_dir.exists() and config_dir.is_dir():
            _delete_fs(config_dir)

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
        cls.assertEqual(cls.ma.get_moduli_dir(), cls.moduli_dir)

    def test_get_candidate_path(cls):
        # Vars for get_candidate_file
        key_length = 2048
        tpath = str(cls.ma.get_moduli_dir().joinpath(f'{key_length}.candidate_'))
        # cp = str(cls.ma.get_candidate_path(key_length))
        cls.assertTrue(tpath in str(cls.ma.get_candidate_path(key_length)))

    def test_get_screened_path(cls):
        key_length = 2048
        cp = cls.ma.get_candidate_path(key_length)
        sp = cls.ma.get_screened_path(cp)
        cls.assertTrue(str(sp).replace('screened', 'candidate') == str(cp.absolute()))

    def test_generate_candidates(cls):
        candidate_file = cls.ma.generate_candidates(2048, 1)
        cls.assertTrue(candidate_file.exists())
        cls.assertTrue(candidate_file.stat().st_size > 1)
        cls.assertTrue(len(candidate_file.read_text().split('\n')) > 50000)

        # Preserve Candidate for Screening Run
        Path('test/resources').joinpath(candidate_file.name).write_text(candidate_file.read_text())
        _store_candidate(candidate_file)

    def test_screen_candidates(cls):
        # Copy Pre-Generated Candidates to Moduli Dir for Screen Testing
        candidate_file = _load_candidate()

        screened_file = cls.ma.screen_candidates(candidate_file)
        cls.assertTrue(screened_file.exists())
        cls.assertTrue(screened_file.stat().st_size > 1)
        cls.assertTrue(len(screened_file.read_text().split('\n')) > 15)

    def test_restart_candidate_screening(cls):
        candidate_file = _load_candidate()
        cls.ma.restart_candidate_screening()
        # cls.assertTrue(cls.ma.screened_path(candidate_file).exists())
        cls.assertTrue(cls.ma.get_screened_path(candidate_file).exists())
        # cls.assertTrue(cls.ma.screened_path(candidate_file).stat().st_size > 1)
        cls.assertTrue(cls.ma.get_screened_path(candidate_file).stat().st_size > 1)
        # cls.assertTrue(len(cls.ma.screened_path(candidate_file).read_text().split('\n')) > 15)
        cls.assertTrue(len(cls.ma.get_screened_path(candidate_file).read_text().split('\n')) > 15)

    def test_write_moduli_file(cls):
        moduli_file = cls.ma.write_moduli_file()
        cls.assertTrue(moduli_file.exists())
        cls.assertTrue(moduli_file.stat().st_size > 1)

    def test_write_named_moduli_file(cls):
        moduli_file = cls.ma.write_moduli_file(cls.ma.config['config_dir'].joinpath('TEST_MODULI_FILE'))
        cls.assertTrue(moduli_file.exists())
        cls.assertTrue(moduli_file.stat().st_size > 1)

    def test_get_version(cls):
        version = cls.ma.version
        cls.assertTrue(cls.ma.version == cls.test_version)
