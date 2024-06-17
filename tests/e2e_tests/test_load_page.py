import time

import eit_dash.definitions.element_ids as ids
from eit_dash.main import app


def test_001_load_page_load_data(dash_duo):
    # start the app
    dash_duo.start_server(app)
    # go to the loading page
    dash_duo.wait_for_page(dash_duo.server_url, timeout=5)
    # click on data type selector
    dash_duo.multiple_click(f"#{ids.INPUT_TYPE_SELECTOR}", clicks=1)
    # select dreager type
    dropdown = dash_duo.find_element(f"#{ids.INPUT_TYPE_SELECTOR}")
    dropdown.send_keys("Draeger")
    # confirm and open
    dash_duo.multiple_click(f"#{ids.SELECT_FILES_BUTTON}", clicks=1)

    # check if the selection popup is open
    assert dash_duo.find_element(f"#{ids.CHOOSE_DATA_POPUP}").is_displayed()

    # navigate to test file
    dash_duo.multiple_click(f"#{ids.PARENT_DIR}", clicks=1)
    # Wait for 10 seconds
    time.sleep(1)
    # click on the test data directory
    dash_duo.multiple_click(
        '[id="\\{\\"index\\"\\:4,\\"type\\"\\:\\"listed_file\\"\\}"]',
        clicks=1,
    )
    # Wait for 10 seconds
    time.sleep(1)
    # click on the test file
    dash_duo.multiple_click(
        '[id="\\{\\"index\\"\\:0,\\"type\\"\\:\\"listed_file\\"\\}"]',
        clicks=1,
    )
    # click confirm button to load the file
    dash_duo.multiple_click(f"#{ids.SELECT_CONFIRM_BUTTON}", clicks=1)

    # Wait for 10 seconds
    time.sleep(10)

    # assert that the periods selector is open
    assert dash_duo.find_element(f"#{ids.DATA_SELECTOR_OPTIONS}").is_displayed()

    # confirm period selection
    dash_duo.multiple_click(f"#{ids.LOAD_CONFIRM_BUTTON}", clicks=1)

    time.sleep(1)
    # check that the card has been created
    assert dash_duo.find_element(f"#{ids.DATASET_CONTAINER}").text != ""
