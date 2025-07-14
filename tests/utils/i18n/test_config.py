def test_fallback_underscore_defined():
    import utils.i18n.config as i18n_config
    assert callable(i18n_config._)
    assert i18n_config._("mensaje") == "mensaje"
