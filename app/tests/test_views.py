import unittest
import pytest
from app.site.views import *

BASE = "http://localhost:5000"

# =========== Departments Views functions TESTING ============

DEP_JSON = {
    "name": "Human Resources"
}

"""Testing `departments()`, `update_department(dep_id)` and `delete_department(dep_id)` view functions"""


# def test_views_departments_get():
#     """GET request to '/departments' route"""
#     r = requests.get(f'{BASE}/departments')
#     assert r.status_code == 200
#     assert r.headers['Content-Type'] == 'text/html; charset=utf-8'
#     assert '<div id="modal_add_department" class="modal fade" role="dialog">' in r.text
#
# def test_views_departments_post_put_delete(app_context):
#     """Adding, updating and deleting Department on the '/departments' route"""
#
#     payload = [('Name', 'Human Resources')]
#
# def test_views_departments_get(app_context):
#     r = app_context.get('/')
#     assert r.status_code == 200
#
# @pytest.mark.usefixtures("client")
# class ViewFunctionsTest:
#
#     def test_views_departments_get(self, client):
#         r = self.client.get('/')
#         self.assertEqual(r.status_code, 200)
#         self.assertEqual(r.headers['Content-Type'], 'text/html; charset=utf-8')


