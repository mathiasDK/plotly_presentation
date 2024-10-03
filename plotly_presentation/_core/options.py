# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2018 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from collections import OrderedDict
import os
from pathlib import Path
import yaml


class Options:
    def __init__(self):
        try:
            options_path = os.environ["PLOTLY_CONFIG_DIR"]
        except KeyError:
            home_path = str(Path.home())
            options_path = home_path + "/.plotly/"
        self._options = OrderedDict(
            {
                "config.options": OptionValue(options_path + "options_config.yaml"),
                "config.callout_settings": OptionValue(options_path + "callout_settings_config.yaml"),
                "config.theme_settings": OptionValue(options_path + "theme_settings_config.yaml"),
                "config.colors": OptionValue(options_path + "colors_config.yaml"),
            }
        )
        default_folder = str(Path.cwd()) + "/plotly_presentation/_core/_defaults/"
        self._default_options = OrderedDict(
            {
                # "config.options": OptionValue(default_folder + "options_config.yaml"),
                "config.callout_settings": OptionValue(default_folder + "callout_settings_config.yaml"),
                "config.theme_settings": OptionValue(default_folder + "theme_settings_config.yaml"),
                "config.colors": OptionValue(default_folder + "colors_config.yaml"),
            }
        )

        # config_filename = self.get_option("config.options")
        # try:
        #     self._from_yaml(config_filename)
        # except FileNotFoundError:
        #     print("Trying defaults")
        #     config_filename = self.get_default_option("config.options")
        #     self._from_yaml(config_filename)

    def get_option(self, option_name):
        """Return the value of the given option"""
        try:
            config_filename = self._get_option(option_name)
            return self._from_yaml(config_filename)
        except FileNotFoundError:
            print("Trying defaults")
            config_filename = self._get_default_option(option_name)
            print(config_filename)
            return self._from_yaml(config_filename)

    def _get_option(self, option_name):
        """Return the value of the given option"""
        return self._options[option_name].value
    
    def _get_default_option(self, option_name):
        """Return the value of the given option"""
        return self._default_options[option_name].value

    @staticmethod
    def _get_value(option_value):
        if isinstance(option_value, OptionValue):
            return option_value.value
        else:
            return option_value

    def _to_yaml(self, filename):
        """Write the options to a yaml file"""
        with open(filename, "w") as outfile:
            yaml.dump(self._options, outfile, default_flow_style=False)

    def _from_yaml(self, filename):
        """Load options from a yaml file.

        Overwrites any options that are specified in the yaml file.
        """
        # Note: We assume that the contents of the config file are trusted
        # TODO: Change this file format to be plain yaml and use SafeLoader
        yaml_options = yaml.load(open(filename), Loader=yaml.UnsafeLoader)
        return yaml_options


class OptionValue:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "%s" % self.value


options = Options()