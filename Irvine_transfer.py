import cloud_webservice as cloudweb
import json

def file_request(file_name):
	clouduplink_ip = "52.240.159.164"
	cloud_webService = cloudweb.cloudWebService(clouduplink_ip)
	status = cloud_webService.get_token()

	if status:
		file_response = cloud_webService.file_request('office','test/',file_name)
		file_response = json.loads(file_response)
		request_status = file_response["status"]

		print file_response

if __name__ == '__main__':
	file_request('ekko_test.txt')