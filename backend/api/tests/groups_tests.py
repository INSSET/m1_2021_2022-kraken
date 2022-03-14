import json
import os
import unittest

from backend.api.model.group import Group

from backend.api import app


def createGroups():
    group1 = Group(
        "10001",
        "group1",
        ["jean", "paul"]
    )
    group2 = Group(
        "10002",
        "group2",
        ["miche", "miche"]
    )
    groups = [group1, group2]
    return groups


class GroupTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        os.system('groupadd -g 10001 ccm1')

    def test_get_groups_success(self):
        response = self.app.get("/api/v1/students", headers={"Content-Type": "application/json"})
        data = json.loads(response.data)

        self.assertEqual(len(data), 1)
        self.assertEqual(200, response.status_code)

    def test_get_group_by_id_success(self):
        response = self.app.get("/api/v1/students/10001", headers={"Content-Type": "application/json"})
        data = json.loads(response.data)

        self.assertEqual(len(data), 1)
        self.assertEqual(200, response.status_code)

    def test_create_group_success(self):
        payload = json.dumps({
            'groupName': 'group1'
        })
        response = self.app.post("/api/v1/students", headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(201, response.status_code)

    def test_create_group_fail(self):
        payload = json.dumps({
            'allo': 'oui'
        })
        response = self.app.post("/api/v1/students", headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(500, response.status_code)

    def tearDown(self):
        os.system('groupdel ccm1')
