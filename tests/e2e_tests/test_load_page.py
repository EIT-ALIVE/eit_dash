import eit_dash.definitions.element_ids as ids

from eit_dash.main import app


def test_001_load_page_load_data(dash_duo):
    # start the app
    dash_duo.start_server(app)
    # go to the loading page
    dash_duo.wait_for_page(dash_duo.server_url + '/load', timeout=5)
    # click the add data button
    dash_duo.multiple_click(f'#{ids.ADD_DATA_BUTTON}', clicks=1)
    # click the select button
    dash_duo.multiple_click(f'#{ids.SELECT_FILES_BUTTON}', clicks=1)
    # click the confirm button
    dash_duo.multiple_click(f'#{ids.LOAD_CONFIRM_BUTTON}', clicks=1)
    # wait for the new card to be added
    dash_duo.wait_for_element_by_id('card-1', timeout=10)
    # assert that the card exists
    assert dash_duo.find_element(f'#{ids.DATASET_CONTAINER}').text != ''
