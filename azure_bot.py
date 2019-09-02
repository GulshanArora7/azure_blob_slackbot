#!/usr/bin/env python3
# Author : Gulshankumar Arora

import os
import time
import sys
import argparse
import requests
import threading
from flask import abort, Flask, jsonify, request
from application.list_blob import BlobFiles
from application.list_blob_files import BlobFilesPattern
from application.slack_post import SlackPost

AZURE_STORAGE_ACCOUNT=''
AZURE_STORAGE_ACCESS_KEY=''

SLACK_VERIFICATION_TOKEN=''

SLACK_BOT_TOKEN = ''

def is_request_valid(request):
    is_token_valid = request.form['token'] == SLACK_VERIFICATION_TOKEN
    return is_token_valid

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Application is UP..!!"


def bot_command(**kwargs):
    time.sleep(5)
    if len(kwargs) <= 5:
        for key, value in kwargs.items():
            account=kwargs['account']
            account_key=kwargs['account_key']
            slack_channel_id=kwargs['slack_channel_id']
            container_name=kwargs['c1']
            number_of_days_old=kwargs['c2']
        action = BlobFiles(account,account_key,container_name,number_of_days_old)
        response = action.azure_blob()
        slack = SlackPost(slack_channel_id, SLACK_BOT_TOKEN, str(response))
        slack.slack_notification()
    elif len(kwargs) > 5:
        for key, value in kwargs.items():
            account=kwargs['account']
            account_key=kwargs['account_key']
            slack_channel_id=kwargs['slack_channel_id']
            container_name=kwargs['c1']
            number_of_days_old=kwargs['c2']
            file_pattern=kwargs['c3'] 
        action = BlobFilesPattern(account,account_key,container_name,number_of_days_old,file_pattern)
        response = action.azure_blob_file()
        slack = SlackPost(slack_channel_id, SLACK_BOT_TOKEN, str(response))
        slack.slack_notification()
    else:
        print("Not entered correct number of arguments")

@app.route('/azure-bot',methods=['POST'])
def azure_bot():
    if not is_request_valid(request):
        abort(400)
    slack_channel_id = request.form.get('channel_id')
    command_text = request.form.get('text')
    command_text = command_text.split(' ')
    if len(command_text) > 1 and len(command_text) <= 2:
        t = threading.Thread(target=bot_command, kwargs={'account': AZURE_STORAGE_ACCOUNT, 'account_key': AZURE_STORAGE_ACCESS_KEY, 'slack_channel_id': slack_channel_id, 'c1': command_text[0], 'c2': command_text[1]})
        t.start()
        return jsonify(
            response_type = "in_channel",
            text='Request is Accepted..Processing it..Please wait..!!',
        )
    elif len(command_text) >= 3:
        t = threading.Thread(target=bot_command, kwargs={'account': AZURE_STORAGE_ACCOUNT, 'account_key': AZURE_STORAGE_ACCESS_KEY, 'slack_channel_id': slack_channel_id, 'c1': command_text[0], 'c2': command_text[1], 'c3': command_text[2]})
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