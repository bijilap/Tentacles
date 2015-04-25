import os
import json
import requests

import config

class Tentacles:

    def read_test_config(self, tname, fname):
        path = "./"+config.TESTS_DIR+"/"+tname+"/"+fname
        conf_file = open(path)
        conf_text = conf_file.read()
        conf_json = json.loads(conf_text)
        return conf_json

    def query_rest_endpoint(self, test_json):
        method = test_json['method']
        url = test_json['url']
        payload = test_json['request']['payload']
        headers = test_json['request']['headers']
        response = None
        if method == "GET":
            response = requests.get(url, data=json.dumps(payload), headers=headers)
        if method == "POST":
            response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response

    def run_validations(self, test_json, response):
        if(str(response.status_code) != test_json["validations"]["status_code"]):
            return False
        return True

    def run_test(self, tname, fname):
        test_json = self.read_test_config(tname, fname)
        print "Test: "+ test_json['name']
        response = self.query_rest_endpoint(test_json)
        test_status = self.run_validations(test_json, response)
        if(test_status == True):
            print "Test passed!"
        else:
            print "Test failed!"

    def deploy(self):
        for roots, dirs, files in os.walk(config.TESTS_DIR, topdown=False):
            for dir in dirs:
                self.execute_tests(dir)

    def execute_tests(self, test_name):
        print "Test Group:    " + test_name
        path = config.TESTS_DIR+"/"+test_name
        for roots, dirs, files in os.walk(config.TESTS_DIR, topdown=False):
            for fname in files:
                self.run_test(test_name, fname)

octopus = Tentacles()
octopus.deploy()
