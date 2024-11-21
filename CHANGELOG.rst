Changelog
=========

2024-11-20
----------

  * ModuliAssembly: '0.10.12'
    * Storing runtime test configurations
    * RC2
    ~r

2024-11-15
----------

  * ModuliAssembly: '0.10.11'
    * Release Candidate
    * Updated Changelong
    * Updated packaging
    ~r
  * ModuliAssembly: '0.10.11'
    * rationalized documentation, completed reformat of produced doc
    ~r

2024-11-14
----------

  * ModuliAssembly: '0.10.11'
    * update changelog.md
    ~r
  * ModuliAssembly: '0.10.11'
    * File and Version Cleanup
    ~r
  * ModuliAssembly: '0.10.11'
    * Pushing Version Wheel and Source Distribution
    ~r
  * ModuliAssembly: '0.10.11'
    * Doc System (Sphinx) Complete and Operational
    * Python Wheel loads properly with all relevant Script Endpoints
    * Successfully Completed FULL run `--all`
    ~r

2024-11-09
----------

  * Update issue templates
  * ModuliAssembly: '0.10.9'
    * Unittests Successful
    * Wheel Installation and Operation Successful
    * Scripts accessible from `poetry run` and python -m moduli_assembly.scripts.*:main
    RC2
    ~r
  * ModuliAssembly: '0.10.8'
    * Unittests Successful
    * Wheel Installation and Operation Successful
    * RC-1
    ~r

2024-11-08
----------

  * ModuliAssembly: '0.10.7'
    * Fixed invalid quotes in f' statements.
    Wheel operating as expected
    ~r

2024-11-05
----------

  * ModuliAssembly: '0.10.1'
    * Checkpoint - Four Unittests Succeed (__init2__) *
    ~r

2024-10-12
----------

  * ModuliAssembly: '0.10.1'
    * Checkpoint *
    ~r

2024-10-08
----------

  * ModuliAssembly: '0.10.1'
    * Checkpoint *
    ~r

2024-10-07
----------

  * ModuliAssembly: '0.10.1'
    * Checkpoint *
    ~r

2024-10-05
----------

  * ModuliAssembly: '0.10.1'
    refactored 'get_moduli_dir' to 'moduli_dir'
    ~r
  * ModuliAssembly: '0.10.1'
    * ModuliAssembly Class Testing Complete and Successful
    ** ModuliAssembly @classmethods
    *** __init__
    *** __del__
    *** create_checkpoint_filename
    *** get_moduli_dir
    *** create_candidate_path
    *** get_screened_path
    *** screen_candidates
    *** write_moduli_file
    *** restart_candidate_screening
    *** clear_artifacts
    *** print_config
    ** Tests
    *** test_ModuliAssembly_default)config
    *** test_ModuliAssembly_missing_attrs
    *** test_get_moduli_dir
    *** test_create_candidate_path
    *** test_get_screened_path
    *** test_generate_candidates
    *** test_screen_candidates
    *** test_restart_canididate_screening
    *** test_write_moduli_file
    *** test_write_named_moduli_file
    *** test_get_version
    ~r
    ~r
  * ModuliAssembly: '0.10.1'
    Tested-by: Python Unittests
    * Successful Checkpoint
    ~r
    ~r

2024-10-03
----------

  * ModuliAssembly: '0.10.0'
    Tested-by: Python Unittests
    * ModuliAssembly.py
    ** default Config
    ** missing attributes
    ** get moduli dir
    ** get candidate path
    ** get screened path
    ** generate and screen candididates
    ~r
    ~r
  * ModuliAssembly: '0.10.0'
    Checkpoint
    ~r

2024-10-01
----------

  * ModuliAssembly: '0.10.0'
    Checkpoint - Successful Tests
    * test_ModuliAssembly_default_config
    * test_ModuliAssembly_missing_attrs
    * test_get_candidate_path
    * test_get_moduli_dir
    * test_get_screened_path
    Failing Tests
    * test_generate_candidates
    ~r

2024-09-30
----------

  * ModuliAssembly: '0.10.0'
    Checkpoint
    ~r

2024-09-24
----------

  * ModuliAssembly: '0.10.0'
    * Build ModuliAssembly classmethods from moduli_assembly functions.
    * Build test_ModuliAssembly from test_moduli_assembly
    TBD - Test Tests ;-}
    ~r

2024-09-23
----------

  * ModuliAssembly: '0.10.0'
    * Checkpoint
    ~r
  * ModuliAssembly: '0.10.0'
    - Converting moduli_assembly to Class
    - Created moduli_assembly.ModuliAssembly Class
    - Created Test Class test_ModuliAssembly.py
    * Class Function Tests
    ** test_Moduli_Assembly_default_config
    ** test_ModuliAssembly_missing_attrs
    ** Mocked all classmethod tests
    ~r

2024-09-22
----------

  * moduli-assembly: v0.9.6
    * test Generate Candidates
    * test Screen Candidates
    - Shortening Candidates for Faster TEST of SCREEN
    ~r

2024-09-21
----------

  * moduli-assembly: v0.9.6
    * Added test_generate_candidates - Successful Unittest
    * Temporariy Enabling 2048 KeyLengths to shorten testing
    2048 no longer considered VERY Secure
    ~r
  * moduli-assembly: v0.9.6
    * added __del__ to Configuration Manager
    ~r
  * moduli-assembly: v0.9.6
    * Refactored Configuration Handler
    * Installed as package moduli_assembly.config_manager
    * Tests installed as package test.config_manager.config_manager
    All Configuration Tests Successful
    ~r

2024-09-16
----------

  * moduli-assembly: v0.9.6
    * Updated Version of Distribution Files
    ~r
  * moduli-assembly: v0.9.6
    * write_moduli_file: Renamed Identifier to `MODULI-ASSEMBLY`
    * Updated Version Number `__main__.py` AND `pyproject.toml`
    * Updated TLDR.md
    * Added `prog` and `description` to ArgumentParser (__main__)
    * Added `version` to Argument Parser (__main__)
    * All Successful Single Action Options end with exit(0) (write_moduli_file, clear_artifacts, rm_config_dir, version)
    ~r

2024-09-14
----------

  * moduli-assembly: v0.9.5
    * README.md - Specified OpenSSH2 (needed for support of `-M generate` and `-M screen` functions.
    ~r
  * moduli-assembly: v0.9.5
    * Cleanup
    ** Removed `randomize_file_record_order` in lieu of using `random.shuffle()` directly when reading
    * Rationalized symlink processing in `write_moduli_file`
    * Standardized File Reads and Writes to
    ** `Path.{read,write}_text()`
    ** and reserving `with Path.open('w') as file` for sequential writes to an accumulator file like ./moduli/`MODULI`
    * Final Edits
    ~r
  * moduli-assembly: v0.9.5
    * Cleanup
    ** Removed `randomize_file_record_order` in lieu of using `random.shuffle()` directly when reading
    * Rationalized symlink processing in `write_moduli_file`
    * Standardized File Reads and Writes to
    ** `Path.{read,write}_text()`
    ** and reserving `with Path.open('w') as file` for sequential writes to an accumulator file like ./moduli/`MODULI`
    ~r

2024-09-12
----------

  * moduli-assembly: v0.9.1,
    operational arguments
    * --bitsizes (gen moduli for modulus size in list
    * --moduli-dir (application root)
    * --moduli-file (file of moduli with safe primes)
    * --all (produce moduli for all supported bitsizes)
    * --clear-artifacts (delete exisiting and screened candidate files)
    * --remove-configuration-dir (delete application configuration)
    * --write-moduli (output moduli from exisiting safe and screened files)
    * --restart (restart all moduli screenings that were previously interrupted)
    * --get-moduli-file (output latest screened Moduli File
    ~r

2024-09-11
----------

  * Completed moduli_assembly_conf.py to manage storage and fetching of application configuration file
    ~r
  * RC 3
    Added Config File Processing: moduli_assembly_conf.py
    * save_conf() and load_conf() Operating Properly
    ~r

2024-09-09
----------

  * RC 2
    * Adding Distribution Directory and Currently Build `sdist` and `wheel` format files.
    ~r
  * Delete dist/moduli_assembly-0.3.1-py3-none-any.whl
  * Delete dist/moduli_assembly-0.3.1.tar.gz
  * RC 2
    * README.md Edits
    ~r
  * RC 2
    * Edited README.md for clarity
    * Verified Exportable Script Operation
    * Verified in module script moduli_infil
    ~r
  * * Added Moduli Infile Endpoint and
    * moduli_infile Bash Script
    ~r
  * Added moduli_infile to profile bit frequencies of moduli
    ~r

2024-09-06
----------

  * * Release Candidate 1
    Package Wheel Loads and Operates properly
    ~r
  * Reformatted Project and Renamed
    Now Supports
    * -a, --all: Generating SSH Moduli Files with all bitsizes [2048, 3072, 4096, 6144, 7680, 8192]
    * -r, --restart: Restarts Interrupted Candididate Screening
    * -w, --write: Writes MODULI File with Currently Screened Candidates
    * -b, --bitsizes [list of authorized bitsizes, multiples generate larger candidate files
    Operational and ready to share
    ~r
  * Initial commit
