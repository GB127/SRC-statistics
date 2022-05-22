from requests_mock.mocker import Mocker
from tests.class_builder import build_category

class Test_category:
    def test_init(self, requests_mock: Mocker):
        category = build_category(requests_mock)
        assert category.__dict__ == {"category" :"Any% (No SSU)", 'ids': ('category_id', [('subcat_id_t', 'selected_subcat')]), "subcategory":["150cc"]}

    def test_getitem(self, requests_mock:Mocker):
        category = build_category(requests_mock)
        assert category["subcategory"] == ["150cc"]

    def test_str(self, requests_mock: Mocker):
        category = build_category(requests_mock)
        assert str(category) == "Any% (No SSU) (150cc)"

