#!/usr/bin/env python3
# Author : Gulshankumar Arora

import os
import time
import sys
import argparse
import requests
import threading

## Note: Comment out below 2 lines if you not running this script manually and assign variable in .env file
#from os.path import join, dirname
#from dotenv import load_dotenv

from flask import abort, Flask, jsonify, request
from application.storage_account_key import STORAGE
from application.list_blob import BlobFiles
from application.list_blob_files import BlobFilesPattern
from application.slack_post import SlackPost

## Note: Comment out below 2 lines if you not running this script manually and assign variable in .env file
#dotenv_path = join(dirname(__file__), '.env')
#load_dotenv(dotenv_path)

subscription_id = os.environ.get("SUBSCRIPTION_ID")
client_id=os.environ.get("CLIENT_ID")
client_secret=os.environ.get("CLIENT_SECRET")
tenant_id=os.environ.get("TENANT_ID")
SLACK_BOT_TOKEN =  os.environ.get("SLACK_BOT_TOKEN")

def is_request_valid(request):
    is_token_valid = request.form['token'] == os.environ.get("SLACK_VERIFICATION_TOKEN")
    return is_token_valid

app = Flask(__name__)

def bot_command(**kwargs):
    time.sleep(5)
    if len(kwargs) <= 6:
        for key, value in kwargs.items():
            slack_channel_id = kwargs['slack_channel_id']
            condition = kwargs['c1']
            number_of_days_old = kwargs['c2']
            resource_group_name = kwargs['c3']
            storage_account_name = kwargs['c4']
            container_name = kwargs['c5']
        storage_details = STORAGE(subscription_id, client_id, client_secret, tenant_id, resource_group_name, storage_account_name)
        storage_account_key = storage_details.azure_storage()
        action = BlobFiles(storage_account_name, storage_account_key, condition, number_of_days_old, container_name)
        response = action.azure_blob()
        slack = SlackPost(slack_channel_id, SLACK_BOT_TOKEN, response)
        slack.slack_notification()
    elif len(kwargs) > 6:
        for key, value in kwargs.items():
            slack_channel_id = kwargs['slack_channel_id']
            condition = kwargs['c1']
            number_of_days_old = kwargs['c2']
            resource_group_name = kwargs['c3']
            storage_account_name = kwargs['c4']
            container_name = kwargs['c5']
            file_pattern = kwargs['c6']
        storage_details = STORAGE(subscription_id, client_id, client_secret, tenant_id, resource_group_name, storage_account_name)
        storage_account_key = storage_details.azure_storage()
        action = BlobFilesPattern(storage_account_name, storage_account_key, condition, number_of_days_old, container_name, file_pattern)
        response = action.azure_blob_file()
        slack = SlackPost(slack_channel_id, SLACK_BOT_TOKEN, response)
        slack.slack_notification()
    else:
        print("Not entered correct number of arguments")

@app.route('/health')
def health_check():
    return "Application is UP..!!"

@app.route('/azure-bot',methods=['POST'])
def azure_bot():
    if not is_request_valid(request):
        abort(400)

    slack_channel_id = os.environ.get('SLACK_CHANNEL_ID')
    command_text = request.form.get('text')
    command_text = command_text.split(' ')
    if len(command_text) > 1 and len(command_text) <= 5:
        t = threading.Thread(target=bot_command, kwargs={'slack_channel_id': slack_channel_id, 'c1': command_text[0], 'c2': str(command_text[1]), 'c3': command_text[2], 'c4': command_text[3], 'c5': command_text[4]})
        t.start()
        return jsonify(
            response_type = "in_channel",
            text='Request is Accepted..Processing it..Please wait..!!',
        )
    elif len(command_text) >= 6:
        t = threading.Thread(target=bot_command, kwargs={'slack_channel_id': slack_channel_id, 'c1': command_text[0], 'c2': str(command_text[1]), 'c3': command_text[2], 'c4': command_text[3], 'c5': command_text[4], 'c6': command_text[5]})
        t.start()
        return jsonify(
            response_type = "in_channel",
            text='Request is Accepted..Processing it..Please wait..!!',
        )
    else:
        return jsonify(
            response_type = "in_channel",
            text = 'Please enter the valid number of argument',
        )

if __name__ == '__main__':
    app.run(debug=False,use_reloader=True,host='0.0.0.0',port=int(os.environ.get('PORT', 9090)))
