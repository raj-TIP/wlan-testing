import ssl
import base64
import urllib.request
from bs4 import BeautifulSoup
import re
from ap_ssh import ssh_cli_active_fw
from lab_ap_info import *


class GetBuild:
    def __init__(self, jfrog_user, jfrog_passwd, build):
        self.user = jfrog_user
        self.password = jfrog_passwd
        ssl._create_default_https_context = ssl._create_unverified_context
        self.jfrog_url = 'https://tip.jfrog.io/artifactory/tip-wlan-ap-firmware/'
        self.build = build

    def get_latest_image(self, model):

        url = self.jfrog_url + model + "/dev/"

        auth = str(
            base64.b64encode(
                bytes('%s:%s' % (self.user, self.password), 'utf-8')
            ),
            'ascii'
        ).strip()
        headers = {'Authorization': 'Basic ' + auth}

        ''' FIND THE LATEST FILE NAME'''
        # print(url)
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        html = response.read()
        soup = BeautifulSoup(html, features="html.parser")

        # find the last pending link on dev
        last_link = soup.find_all('a', href=re.compile(self.build))[-1]
        latest_file = last_link['href']
        latest_fw = latest_file.replace('.tar.gz', '')
        return latest_fw

    def check_latest_fw(self, ap_model=None):
        for model in ap_models:
            if model == ap_model:
                return self.get_latest_image(model)
            else:
                continue
