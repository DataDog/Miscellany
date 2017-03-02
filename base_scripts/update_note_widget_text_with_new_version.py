#!/usr/bin/env python
"""
 Provides a simple way to update a version number on a screenboard.
 This script is unintelligent in the sense that it parses a screenboard
 looking for the html field in a note widget with the text 'version'. Once
 it finds this it will update version number.

 This script can be called from the command-line, but this just sets
 DEBUG mode. Could easily be modified to be passed in a version.

 Intended to be run during a release or update so the screenboard
 reflects the current version of an applications
"""

from datadog import initialize, api
import logging
import argparse

def initialize_api(api_key, app_key):
    options = {
            'api_key': api_key,
            'app_key': app_key
            }

    initialize(**options)

def modify_note_version_widget(board_json, VERSION):

    widgets_to_update = []
    widgets_to_maintain = []
    for widget in board_json['widgets']:
        try:
            # Note widget includes field 'html' that contains the text displayed
            logging.debug(widget)
            if "version" in widget['html'].lower():
                logging.info("Updating widget")
                widget['html'] = 'Version: {0}'.format(VERSION)
                widgets_to_update.append(widget)

        except KeyError:
            # We do not care about other widgets, but the ids need to be appended
            widgets_to_maintain.append(widget)
            pass

    return widgets_to_update, widgets_to_maintain

def main():

    logger = logging.getLogger(__name__)

    API_KEY = ''
    APP_KEY = ''
    logging.info('Initializing API')
    initialize_api(API_KEY, APP_KEY)

    # Screenboard ID - can be found in URL
    board_id =
    VERSION = ''
    BOARD_TITLE = 'Dashboard title TEST'

    logging.info('GETing board from API')
    # Get the JSON of the screenboard
    board_to_update = api.Screenboard.get(board_id)
    logging.debug("Printing board:")
    logging.debug(board_to_update)

    logging.info('Running function to update widget')
    # Parse through the board's JSON and modify note widget
    updated_widgets, maintained_widgets = modify_note_version_widget(board_to_update, VERSION)


    logging.debug("Printing update_widgets list")
    logging.debug(updated_widgets)

    logging.debug("Printing maintained widgets list:")
    logging.debug(maintained_widgets)

    logging.info("Concatenating widget lists")
    widgets = updated_widgets + maintained_widgets

    logging.info('Running update call to API')

    # Send updated widgets
    result = api.Screenboard.update(board_id, board_title=BOARD_TITLE, widgets=widgets)
    logging.info("Printing result:")
    logging.info(result)

def setup_command_line_parser():
    """
        Sets up command line argument parser. Additional arguments could be added
        easily. For example if the version needed to be passed in with -v you
        could add it as a positional argument like so:
        parser.add_argument("-v", "--version", help="Current version of application"
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action='store_true', help="Run script in debug mode")
    args = parser.parse_args()
    return parser

if __name__ == "__main__":

    parser = setup_command_line_parser()

    args = parser.parse_args()
    # Check to see if we want to run as debug
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    main()
