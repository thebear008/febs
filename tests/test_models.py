""" test models """

from models.models import MainModel


def test_init_main_model():
    """ test init method for MainModel """
    my_object = MainModel()
    assert my_object._config is None
    assert my_object._bucket is None
