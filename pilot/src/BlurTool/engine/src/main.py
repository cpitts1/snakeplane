# Copyright (C) 2019 Alteryx, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# 3rd Party Libraries
import AlteryxPythonSDK as sdk

import pandas as pd

from scipy import ndimage

from snakeplane.plugin_factory import PluginFactory

# Initialization of the plug in factory, used for making the AyxPlugin class
factory = PluginFactory("BlurTool")


@factory.initialize_plugin
def init(input_mgr, user_data, logger):
    """Initialize the example source tool."""
    # Get the selected value from the GUI and save it for later use in the user_data
    user_data.val = float(input_mgr.workflow_config["Value"])

    # Display info on the selected value
    logger.display_info_msg(f"The value selected is {user_data.val}")

    return True


@factory.process_data(mode="batch", input_type="dataframe")
def process_data(input_mgr, output_mgr, user_data, logger):
    """Generate some data to source."""
    # Grab the input anchor
    input_anchor = input_mgr["Input"][0]

    # Get the data out of it in the form of a dataframe
    input_data = input_anchor.data
    blur_array = input_data.values

    # Blur the data using the user's input for sigma
    output_array = ndimage.gaussian_filter(blur_array, sigma=user_data.val)

    # Create output dataframe by putting new array in a dataframe form
    output_data = pd.DataFrame(output_array)

    # Set the output data for the Output anchor
    data_out = output_mgr["Output"]
    data_out.data = output_data


@factory.build_metadata
def build_metadata(input_mgr, output_mgr, user_data, logger):
    """Build metadata for blur tool."""

    # Grab the input anchor connection
    input_anchor = input_mgr["Input"][0]

    # Get the input anchors metadata
    input_metadata = input_anchor.metadata

    # Reassign to the output metadata variable
    output_metadata = input_metadata

    # Assign to the output anchor
    output_anchor = output_mgr["Output"]
    output_anchor.metadata = output_metadata


AyxPlugin = factory.generate_plugin()
