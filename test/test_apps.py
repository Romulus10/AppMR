from appMR.apps import AppmrConfig


def test_main_config():
    assert AppmrConfig.name == "appMR"
