# vim: expandtab:ts=4:sw=4

import os, sys
import commands as cm
import hashlib
import urllib, urllib2
import json

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import ssl

class cloudWebService:
    def __init__(self, clouduplink_ip):
        ssl._create_default_https_context = ssl._create_unverified_context
        self.clouduplink_ip = clouduplink_ip
        m = hashlib.md5()
        m.update('Xjtu123456')
        pwd = m.hexdigest()
        self.username = "admin"
        self.values = {'username': 'admin', 'password': pwd, 'task': ''}
        self.token = ''

    def get_token(self):
        # get request
        self.values.update({'task': 'get'})
        values_url = urllib.urlencode(self.values)
        url = 'https://' + self.clouduplink_ip + '/configurator/token.php' + '?' + values_url
        #print url
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            response = response.read()
            response = json.loads(response)
            status = response["status"]

            if 'success' == status:
                self.token = response["token"]
                return True
            else:
                return False

        except:
            return False

    # fileCloud_path = "uplinktest/"
    # container_name = "office"
    # file_name = "test.jpg"
    def file_request(self, container_name,fileCloud_path,file_name):
        # post request
        url = "https://" + self.clouduplink_ip + "/webservice/update.php"
        register_openers()
        try:
            token = self.token
            datagen, headers = multipart_encode(
                {"task": 'file_request', 'username': self.username, 'token': token,
                 "filetoupload": open(file_name, "rb"),
                 "fileCloud_path": fileCloud_path, "container_name": container_name})
            request = urllib2.Request(url, datagen, headers)

            response = urllib2.urlopen(request).read()
            print response
            # response = json.loads(response)

            return response
            print "upload file ok"
        except:
            response = {'status': 'fail', 'fileCloud': ''}
            response = json.dumps(response)
            return response

    def sql_request(self,sql,dbname):
        # post request
        url = "https://" + self.clouduplink_ip + "/webservice/update.php"
        register_openers()
        try:
            token = self.token
            datagen, headers = multipart_encode({"task": 'sql_request', 'username': self.username, 'token': token,
                                                 'sql': sql, 'dbname': dbname})
            request = urllib2.Request(url, datagen, headers)

            response = urllib2.urlopen(request).read()

            #print response
            return response
        # response = json.loads(response)
        except:
            response = {'status': 'fail', 'fileCloud': ''}
            response = json.dumps(response)
            return response


    def sql_inserts(self,sql,dbname):
        # post request
        url = "https://" + self.clouduplink_ip + "/webservice/update.php"
        register_openers()
        try:
            token = self.token
            datagen, headers = multipart_encode({"task": 'sql_inserts', 'username': self.username, 'token': token,
                                                 'sql': sql, 'dbname': dbname})
            request = urllib2.Request(url, datagen, headers)

            response = urllib2.urlopen(request).read()

            print response
            return response
        # response = json.loads(response)
        except:
            response = {'status': 'fail', 'fileCloud': ''}
            response = json.dumps(response)
            return response

    def get_token_http(self):
        # get request
        self.values.update({'task': 'get'})
        values_url = urllib.urlencode(self.values)
        url = 'http://' + self.clouduplink_ip + '/configurator/token.php' + '?' + values_url
        print url
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            response = response.read()
            response = json.loads(response)
            status = response["status"]

            if 'success' == status:
                self.token = response["token"]
                return True
            else:
                return False

        except:
            return False

    # fileCloud_path = "uplinktest/"
    # container_name = "office"
    # file_name = "test.jpg"
    def file_request_http(self, container_name,fileCloud_path,file_name):
        # post request
        url = "http://" + self.clouduplink_ip + "/webservice/update.php"
        register_openers()

        try:
            token = self.token
            datagen, headers = multipart_encode(
                {"task": 'file_request', 'username': self.username, 'token': token,
                 "filetoupload": open(file_name, "rb"),
                 "fileCloud_path": fileCloud_path, "container_name": container_name})
            request = urllib2.Request(url, datagen, headers)

            response = urllib2.urlopen(request).read()
            print response
            # response = json.loads(response)

            return response
            print "upload file ok"
        except:
            response = {'status': 'fail', 'fileCloud': ''}
            response = json.dumps(response)
            return response


    def sql_request_http(self,sql,dbname):
        # post request
        url = "http://" + self.clouduplink_ip + "/webservice/update.php"
        register_openers()
        try:
            token = self.token
            datagen, headers = multipart_encode({"task": 'sql_request', 'username': self.username, 'token': token,
                                                 'sql': sql, 'dbname': dbname})
            request = urllib2.Request(url, datagen, headers)

            response = urllib2.urlopen(request).read()
            print response
            # response = json.loads(response)

            return response

        except:
            response = {'status': 'fail', 'fileCloud': ''}
            response = json.dumps(response)
            return response



