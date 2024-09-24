__version__ = '0.10.0'

from datetime import datetime, timezone

from moduli_assembly.config_manager.config_manager import ConfigManager


def ISO_UTC_TIMESTAMP() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def _default_config():
    """
    tbd - REMOVE Keylength 2048 BEFORE PRODUCTION
    :return:
    :rtype:
    """
    return {
        "generator_type": 2,
        "auth_bitsizes": ["2048", "3072", "4096", "6144", "7680", "8192"],
        "config_dir": ".moduli_assembly",
        "config_file": ".config",
        "moduli_dir": ".moduli"
    }


class ModuliAssembly(ConfigManager):

    @classmethod
    def version(cls) -> str:
        return __version__

    @classmethod
    def __init__(cls, config: dict = None) -> None:
        if config:
            cls.config = config
        else:
            cls.config = _default_config()

        for attr in ['config_dir', 'config_file', 'moduli_dir', 'generator_type', 'auth_bitsizes']:
            if attr not in cls.config:
                raise AttributeError(f'Config Required Attribute: {attr}')

        super().__init__(cls.config)

    def __del__(self):
        """
        Override ConfigManager's __del__
        :return:
        :rtype:
        """
        pass

    @classmethod
    def get_moduli_dir(cls):
        pass

    @classmethod
    def get_candidate_path(cls):
        pass

    @classmethod
    def get_screened_path(cls):
        pass

    @classmethod
    def screen_candidates(cls):
        pass

    @classmethod
    def generate_candidates(cls):
        pass

    @classmethod
    def write_moduli_file(cls):
        pass

    @classmethod
    def restart_candidate_screening(cls):
        pass

    @classmethod
    def clear_artifacts(cls):
        pass


def main():
    # __init__
    ma = ModuliAssembly()


if __name__ == '__main__':
    main()
