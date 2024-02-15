from unittest.mock import MagicMock, Mock, patch

import pytest

from functions.functions import set_app_id_via_selected_app_name


@pytest.mark.parametrize(
    "expected_app_id, selected_app_name, app_list",
    [
        ("a1", "some_first_app", [{"app_name": "some_first_app", "app_id": "a1"}, {"app_name": "some_second_app", "app_id": "a2"}]),
        ("a2", "some_second_app", [{"app_name": "some_first_app", "app_id": "a1"}, {"app_name": "some_second_app", "app_id": "a2"}])
    ]
)
def test_set_app_id_via_selected_app_name(expected_app_id, selected_app_name, app_list):
    with patch('streamlit.session_state', new_callable=dict) as mock_st:
        mock_st["selected_app_name"] = selected_app_name
        mock_st["app_list"] = app_list

        sut = set_app_id_via_selected_app_name

        assert sut() == expected_app_id


