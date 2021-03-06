#!/usr/bin/python3 -u

# Example to set profile on NOLA-12 testbed:
# ./sdk_set_profile.py --testrail-user-id NONE --model ecw5410 --ap-jumphost-address localhost --ap-jumphost-port 8823 --ap-jumphost-password pumpkin77 \
#                     --ap-jumphost-tty /dev/ttyAP1 --testbed "NOLA-12" --lanforge-ip-address localhost --lanforge-port-number 8822 \
#                     --default-ap-profile TipWlan-2-Radios --sdk-base-url https://wlan-portal-svc-ben-testbed.cicd.lab.wlan.tip.build --skip-radius

# Example to set profile on NOLA-01 testbed
# ./sdk_set_profile.py --testrail-user-id NONE --model ecw5410 --ap-jumphost-address localhost --ap-jumphost-port 8803 \
#   --ap-jumphost-password pumpkin77 --ap-jumphost-tty /dev/ttyAP1 --testbed "NOLA-01" --lanforge-ip-address localhost \
#   --lanforge-port-number 8802 --default-ap-profile TipWlan-2-Radios --sdk-base-url https://wlan-portal-svc.cicd.lab.wlan.tip.build \
#   --skip-radius

import sys

sys.path.append(f'../tests')

from UnitTestBase import *
from cloudsdk import CreateAPProfiles




def main():



    parser = argparse.ArgumentParser(description="SDK Set Profile", add_help=False)
    parser.add_argument("--default-ap-profile", type=str,
                        help="Default AP profile to use as basis for creating new ones, typically: TipWlan-2-Radios or TipWlan-3-Radios",
                        required=True)
    parser.add_argument("--skip-radius", dest="skip_radius", action='store_true',
                        help="Should we skip the RADIUS configs or not")
    parser.add_argument("--skip-wpa", dest="skip_wpa", action='store_true',
                        help="Should we skip the WPA ssid or not")
    parser.add_argument("--skip-wpa2", dest="skip_wpa2", action='store_true',
                        help="Should we skip the WPA2 ssid or not")
    parser.set_defaults(skip_radius=False)
    parser.set_defaults(skip_wpa=False)
    parser.set_defaults(skip_wpa2=False)
    parser.add_argument("--skip-profiles", dest="skip_profiles", action='store_true',
                        help="Should we skip creating new ssid profiles?")
    parser.set_defaults(skip_profiles=False)

    parser.add_argument("--psk-5g-wpa2", type=str,
                        help="Allow over-riding the 5g-wpa2 PSK value.")
    parser.add_argument("--psk-5g-wpa", type=str,
                        help="Allow over-riding the 5g-wpa PSK value.")
    parser.add_argument("--psk-2g-wpa2", type=str,
                        help="Allow over-riding the 2g-wpa2 PSK value.")
    parser.add_argument("--psk-2g-wpa", type=str,
                        help="Allow over-riding the 2g-wpa PSK value.")

    parser.add_argument("--ssid-5g-wpa2", type=str,
                        help="Allow over-riding the 5g-wpa2 SSID value.")
    parser.add_argument("--ssid-5g-wpa", type=str,
                        help="Allow over-riding the 5g-wpa SSID value.")
    parser.add_argument("--ssid-2g-wpa2", type=str,
                        help="Allow over-riding the 2g-wpa2 SSID value.")
    parser.add_argument("--ssid-2g-wpa", type=str,
                        help="Allow over-riding the 2g-wpa SSID value.")







    base = UnitTestBase("skd-set-profile", parser)

    command_line_args = base.command_line_args

    # cmd line takes precedence over env-vars.
    cloudSDK_url = command_line_args.sdk_base_url  # was os.getenv('CLOUD_SDK_URL')
    local_dir = command_line_args.local_dir  # was os.getenv('SANITY_LOG_DIR')
    report_path = command_line_args.report_path  # was os.getenv('SANITY_REPORT_DIR')
    report_template = command_line_args.report_template  # was os.getenv('REPORT_TEMPLATE')

    ## TestRail Information
    tr_user = command_line_args.testrail_user_id  # was os.getenv('TR_USER')
    tr_pw = command_line_args.testrail_user_password  # was os.getenv('TR_PWD')
    milestoneId = command_line_args.milestone  # was os.getenv('MILESTONE')
    projectId = command_line_args.testrail_project  # was os.getenv('PROJECT_ID')
    testRunPrefix = command_line_args.testrail_run_prefix  # os.getenv('TEST_RUN_PREFIX')

    ##Jfrog credentials
    jfrog_user = command_line_args.jfrog_user_id  # was os.getenv('JFROG_USER')
    jfrog_pwd = command_line_args.jfrog_user_password  # was os.getenv('JFROG_PWD')

    ##EAP Credentials
    identity = command_line_args.eap_id  # was os.getenv('EAP_IDENTITY')
    ttls_password = command_line_args.ttls_password  # was os.getenv('EAP_PWD')

    ## AP Credentials
    ap_username = command_line_args.ap_username  # was os.getenv('AP_USER')

    ##LANForge Information
    lanforge_ip = command_line_args.lanforge_ip_address
    lanforge_port = command_line_args.lanforge_port_number
    lanforge_prefix = command_line_args.lanforge_prefix
    lanforge_2g_radio = command_line_args.lanforge_2g_radio
    lanforge_5g_radio = command_line_args.lanforge_5g_radio

    build = command_line_args.build_id

    logger = base.logger
    hdlr = base.hdlr

    if command_line_args.testbed == None:
        print("ERROR:  Must specify --testbed argument for this test.")
        sys.exit(1)

    client: TestRail_Client = TestRail_Client(command_line_args)

    ###Get Cloud Bearer Token
    cloud: CloudSDK = CloudSDK(command_line_args)
    bearer = cloud.get_bearer(cloudSDK_url, cloud_type)

    cloud.assert_bad_response = True

    model_id = command_line_args.model
    equipment_id = command_line_args.equipment_id

    print("equipment-id: %s" % (equipment_id))

    if equipment_id == "-1":
        eq_id = ap_ssh_ovsh_nodec(command_line_args, 'id')
        print("EQ Id: %s" % (eq_id))

        # Now, query equipment to find something that matches.
        eq = cloud.get_customer_equipment(cloudSDK_url, bearer, customer_id)
        for item in eq:
            for e in item['items']:
                print(e['id'], "  ", e['inventoryId'])
                if e['inventoryId'].endswith("_%s" % (eq_id)):
                    print("Found equipment ID: %s  inventoryId: %s" % (e['id'], e['inventoryId']))
                    equipment_id = str(e['id'])

    if equipment_id == "-1":
        print("ERROR:  Could not find equipment-id.")
        sys.exit(1)

    ###Get Current AP Firmware and upgrade
    try:
        ap_cli_info = ssh_cli_active_fw(command_line_args)
        ap_cli_fw = ap_cli_info['active_fw']
    except Exception as ex:
        print(ex)
        logging.error(logging.traceback.format_exc())
        ap_cli_info = "ERROR"
        print("FAILED:  Cannot Reach AP CLI.");
        sys.exit(1)

    fw_model = ap_cli_fw.partition("-")[0]


    print('Current Active AP FW from CLI:', ap_cli_fw)

    ###Find Latest FW for Current AP Model and Get FW ID

    ############################################################################
    #################### Create Report #########################################
    ############################################################################

    # Create Report Folder for Today
    today = str(date.today())
    try:
        os.mkdir(report_path + today)
    except OSError:
        print("Creation of the directory %s failed" % report_path)
    else:
        print("Successfully created the directory %s " % report_path)

    logger.info('Report data can be found here: ' + report_path + today)

    ##Get Bearer Token to make sure its valid (long tests can require re-auth)
    bearer = cloud.get_bearer(cloudSDK_url, cloud_type)
    radius_name = "%s-%s-%s" % (command_line_args.testbed, fw_model, "Radius")
    obj = CreateAPProfiles(command_line_args, cloud=cloud, client=client, fw_model=fw_model)


    # Allow cmd-line to override
    if command_line_args.psk_5g_wpa2:
        obj.psk_data["5g"]["wpa2"]["name"] = command_line_args.psk_5g_wpa2
        obj.psk_data["5g"]["wpa2"]["nat"] = command_line_args.psk_5g_wpa2
        obj.psk_data["5g"]["wpa2"]["vlan"] = command_line_args.psk_5g_wpa2
    if command_line_args.psk_5g_wpa:
        obj.psk_data["5g"]["wpa"]["name"] = command_line_args.psk_5g_wpa
        obj.psk_data["5g"]["wpa"]["nat"] = command_line_args.psk_5g_wpa
        obj.psk_data["5g"]["wpa"]["vlan"] = command_line_args.psk_5g_wpa
    if command_line_args.psk_2g_wpa2:
        obj.psk_data["2g"]["wpa2"]["name"] = command_line_args.psk_2g_wpa2
        obj.psk_data["2g"]["wpa2"]["nat"] = command_line_args.psk_2g_wpa2
        obj.psk_data["2g"]["wpa2"]["vlan"] =command_line_args.psk_2g_wpa2
    if command_line_args.psk_2g_wpa:
        obj.psk_data["2g"]["wpa"]["name"] = command_line_args.psk_2g_wpa
        obj.psk_data["2g"]["wpa"]["nat"] = command_line_args.psk_2g_wpa
        obj.psk_data["2g"]["wpa"]["nat"] = command_line_args.psk_2g_wpa
    if command_line_args.ssid_5g_wpa2:
        obj.ssid_data["5g"]["wpa2"]["name"] = command_line_args.ssid_5g_wpa2
        obj.ssid_data["5g"]["wpa2"]["nat"] = command_line_args.ssid_5g_wpa2
        obj.ssid_data["5g"]["wpa2"]["vlan"] = command_line_args.ssid_5g_wpa2
    if command_line_args.ssid_5g_wpa:
        obj.ssid_data["5g"]["wpa"]["name"] = command_line_args.ssid_5g_wpa
        obj.ssid_data["5g"]["wpa"]["nat"] = command_line_args.ssid_5g_wpa
        obj.ssid_data["5g"]["wpa"]["vlan"] = command_line_args.ssid_5g_wpa
    if command_line_args.ssid_2g_wpa2:
        obj.ssid_data["2g"]["wpa2"]["name"] = command_line_args.ssid_2g_wpa2
        obj.ssid_data["2g"]["wpa2"]["nat"] = command_line_args.ssid_2g_wpa2
        obj.ssid_data["2g"]["wpa2"]["vlan"] = command_line_args.ssid_2g_wpa2
    if command_line_args.ssid_2g_wpa:
        obj.ssid_data["2g"]["wpa"]["name"] = command_line_args.ssid_2g_wpa
        obj.ssid_data["2g"]["wpa"]["nat"] = command_line_args.ssid_2g_wpa
        obj.ssid_data["2g"]["wpa"]["vlan"] = command_line_args.ssid_2g_wpa

    print("creating Profiles")
    ssid_template = "TipWlan-Cloud-Wifi"



    if not command_line_args.skip_profiles:
        if not command_line_args.skip_radius:
            obj.create_radius_profile(radius_name, rid, key)
        obj.create_ssid_profiles(ssid_template=ssid_template, skip_wpa2=command_line_args.skip_wpa2,
                                 skip_wpa=command_line_args.skip_wpa, skip_eap=command_line_args.skip_radius)

    print("Create AP with equipment-id: ", equipment_id)
    obj.create_ap_bridge_profile(eq_id=equipment_id, fw_model=fw_model)
    obj.validate_changes()

    print("Profiles Created")

main()

