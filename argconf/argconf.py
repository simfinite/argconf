#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""argconf.py: Generate commandline interfaces for your Python scripts from YAML
configuration files."""

import yaml
import argparse
import argcomplete
import string


def str2bool(v):
    """Convert a string to a boolean value."""
    # Deliberately taken from:
    # https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ValueError('Boolean value expected.')


def get_value(config, key):
    """Get value from (possibly nested) configuration dictionary by using a
    single string key as used for the commandline interface (list of keys
    delimited by '-' or '_').
    """
    keys = key.replace('-', '_').split('_')
    for key in keys[:-1]:
        config = config[key]
    return config[keys[-1]]


def format(format_str, config):
    # parse returns tuple: (literal_text, field_name, format_spec, conversion)
    fields = [f for f in string.Formatter().parse(format_str)
              if f[1] is not None]
    pos_args = [f for f in fields if not f[1]]
    if pos_args:
        raise ValueError("Format string contains positional arguments.")
    values = {f[1]: get_value(config, f[1]) for f in fields if f[1]}
    missing_fields = [f[1] for f in fields if f[1] not in values]
    if missing_fields:
        raise ValueError("Failed to format fields in format string: {}".format(
            missing_fields))
    return string.Formatter().vformat(format_str, args=[], kwargs=values)


def get_yaml_config(yaml_file):
    """Open and parse a YAML configuration file into a dict."""
    with open(yaml_file, 'r') as config_file:
        try:
            config = yaml.load(config_file)
            return config
        except yaml.YAMLError as exc:
            print("Failed to parse YAML configuration file: {}".format(exc))
            return {}


def add_argument(parser, key, value, group):
    # Make argument string as to be typed on the commandline
    if group:
        arg_string = "--{}-{}".format(group, key)
    else:
        arg_string = "--{}".format(key)
    # Make help string
    help_string = "type: {}".format(type(value).__name__)
    # Handle different types
    if type(value) is list:
        parser.add_argument(
            arg_string, help=help_string, nargs="*")
    elif type(value) in (int, float, str):
        parser.add_argument(
            arg_string, type=type(value), help=help_string)
    elif type(value) is bool:
        parser.add_argument(
            arg_string, type=str2bool, nargs='?', const=True, help=help_string)
    else:
        raise ValueError("Type not supported: {}".format(type(value).__name__))


def add_arguments(parser, config_dict, group=""):
    if group:
        parser = parser.add_argument_group(group)
    for key, value in config_dict.iteritems():
        if isinstance(value, dict):
            # Recurse into nested dictionary
            nested_group = group+"-{}".format(key) if group else key
            add_arguments(parser, value, nested_group)
        else:
            add_argument(parser, key, value, group)


def get_parser(config):
    parser = argparse.ArgumentParser()
    add_arguments(parser, config)
    return parser


def match_config_keys(config, arg_string):
    arg_string = arg_string.strip('-_')
    matched_keys = []
    for key, value in config.iteritems():
        if arg_string.find(key) == 0:
            matched_keys.append(key)
            if isinstance(value, dict):
                # Recurse
                arg_string_rest = arg_string.split(key)[1]
                matched_keys += match_config_keys(value, arg_string_rest)
    return matched_keys


def get_cli_config(config, parsed_args):
    # Get a dictionary from parsed args containing all given arguments
    args_dict = vars(parsed_args)
    args_dict = {k: v for k, v in args_dict.iteritems() if v is not None}
    args_dict_resolved = {}
    for key, value in args_dict.iteritems():
        cfg_keys = match_config_keys(config, key)
        target_dict = args_dict_resolved
        for key in cfg_keys[:-1]:
            if key not in target_dict:
                target_dict[key] = {}
            target_dict = target_dict[key]
        target_dict[cfg_keys[-1]] = value
    return args_dict_resolved


def update_config(config, cli_config):
    # Update from inner-most to outer-most dictionary
    for key, value in cli_config.iteritems():
        if isinstance(value, dict):
            # Recurse
            update_config(config[key], value)
        else:
            config[key] = value
    return config


def get_config(parser, config):
    parsed_args = parser.parse_args()
    cli_config = get_cli_config(config, parsed_args)
    config = update_config(config, cli_config)
    return config


def parse_config(yaml_file):
    config = get_yaml_config(yaml_file)
    parser = get_parser(config)
    argcomplete.autocomplete(parser)
    config = get_config(parser, config)
    return config
