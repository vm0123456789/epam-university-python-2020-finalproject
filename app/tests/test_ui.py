# import pytest
# from selenium import webdriver
# import time
#
# BASE = "http://localhost:5000"
#
#
# @pytest.fixture()
# def chrome_browser(scope="function"):
#     driver = webdriver.Chrome(executable_path='app/tests/drivers/chromedriver')
#     driver.maximize_window()
#     yield driver
#     driver.close()
#
#
# t = 2  # selenium web driver's sleep time
#
#
# def test_views_departments_post_put_delete(chrome_browser):
#     """Adding, updating and deleting Department on the '/departments' route"""
#
#     # POST method. Add new department 'Human Resources'
#
#     driver = chrome_browser
#     driver.get(f'{BASE}/departments')
#     time.sleep(t)
#
#     link_to_add_department_form = driver.find_element_by_id("add_department_form_button")
#     link_to_add_department_form.click()
#     time.sleep(t)
#
#     add_department_form_textfield = driver.find_element_by_css_selector(
#         "#AddDepartmentForm > div:nth-child(1) > input:nth-child(2)")
#     add_department_form_textfield.send_keys('Human Resources')
#     add_department_form_submit = driver.find_element_by_css_selector("#btnAddDepartment")
#     add_department_form_submit.click()
#     time.sleep(t)
#
#     link_to_edit_department_form = driver.find_element_by_css_selector(
#         "div.flexbox_item:nth-child(7) > div:nth-child(3) > a:nth-child(1)")
#     link_to_edit_department_form.click()
#     time.sleep(t)
#
#     edit_department_form_textfield = driver.find_element_by_css_selector(
#         '#modal_edit_department4 > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > form:nth-child(1) > div:nth-child(1) > input:nth-child(2)')
#     edit_department_form_textfield.clear_field()
#     edit_department_form_textfield.send_keys('Human Resources (HR)')
#     edit_department_form_submit = driver.find_element_by_css_selector("#btnEditDepartment")
#     edit_department_form_submit.click()
#     time.sleep(t)
