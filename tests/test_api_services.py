from services.api_services import get_app_list


def test_get_app_list():
    sut = get_app_list
    app_list = sut()

    for app in app_list:
        assert 'app_name' in app
        assert 'app_id' in app


