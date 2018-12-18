===========
argconf
===========

*Parametrize all the things!*

argconf generates commandline interfaces for your Python scripts from YAML
configuration files. It is based on argparse and argcomplete.

After writing a YAML configuration file for your script, add the following line
to retrieve a configuration dictionary that will default to the file's content,
but include any user input given via the commandline:

``
    import argconf
    config = argconf.parse('your_config.yaml')
``

Your script will now feature a generated commandline interface, which you can
checkout by running ``your_script.py --help``.

In order to get *tab completion*, argcomplete has to be globally activated (see
[https://argcomplete.readthedocs.io/en/latest/#activating-global-completion]).
Also, '# PYTHON_ARGCOMPLETE_OK' has to added to the script's header comment
block.

TODO
----

- Support more YAML types (see http://yaml4r.sourceforge.net/doc/page/basic_types_in_yaml.htm)
- Add help strings based on comments in the configuration file to the cli
  (maybe based on alternative YAML parser 'ruamel')
- Support other configuration file formats: JSON, XML
- Make argcomplete and configuration file parser (e.g. pyyaml) optional deps.
- Add Python 3 support
- Add API documentation
- Add unit tests
- Package and release on PyPI
