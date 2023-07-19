import eit_dash.definitions.element_ids as ids
import dash
from dash import html
from eit_dash.main import app


# 2. give each testcase a test case ID, and pass the fixture
# dash_duo as a function argument
def test_001_child_with_0(dash_duo):
    # 3. define your app inside the test function
    # 4. host the app locally in a thread, all dash server configs could be
    # passed after the first app argument
    dash_duo.start_server(app)
    # 5. use wait_for_* if your target element is the result of a callback,
    # keep in mind even the initial rendering can trigger callbacks
    dash_duo.wait_for_page(dash_duo.server_url + '/load', timeout=5)
    # 6. use this form if its present is expected at the action point
    dash_duo.multiple_click(f'#{ids.ADD_DATA_BUTTON}', clicks=1)
    dash_duo.multiple_click(f'#{ids.SELECT_FILES_BUTTON}', clicks=1)
    dash_duo.multiple_click(f'#{ids.LOAD_CONFIRM_BUTTON}', clicks=1)
    dash_duo.wait_for_element_by_id('card-1')
    assert dash_duo.find_element(f'#{ids.DATASET_CONTAINER}').text != ''
    # 8. visual testing with percy snapshot
    dash_duo.percy_snapshot("test_001_child_with_0-layout")
