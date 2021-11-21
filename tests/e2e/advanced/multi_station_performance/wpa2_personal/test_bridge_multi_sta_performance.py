import pytest
import allure
import os
import time
import pandas as pd

pytestmark = [pytest.mark.advance, pytest.mark.multistaperf, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}
        ]
    },
    "rf": {},
    "radius": False
}
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestMultiStaPerfBridge(object):

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5733", name="WIFI-5733")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_multi_station_tcp_upload_short_dis_nss1_2g(self, lf_test, lf_tools):
        # run wifi capacity test here
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        sta = ["1.1.sta0000", "1.1.sta0001", "1.1.sta0003"]
        atten_value = 100
        lf_tools.set_radio_antenna("cli-json/set_wifi_radio", 1, 1, lf_tools.two_radios[0], 1)
        lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"], radio=lf_tools.two_radios[0], station_name=sta)
        lf_tests.attenuator_modify("all", "all", atten_value)
        #lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="tcp_upload_short_dis_nss1_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="3",
                                        upload_rate="4Mbps", protocol="TCP-IPv4", duration="120000", create_stations=False)


        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-5733", name="WIFI-5733")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_multi_station_tcp_upload_short_med_dis_nss1_2g(self, lf_test, lf_tools):
        # run wifi capacity test here
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        sta = [["1.1.sta0000", "1.1.sta0001", "1.1.sta0003"], ["1.1.sta0004", "1.1.sta0005", "1.1.sta0006"]]

        for i in range(2):
            lf_tools.set_radio_antenna("cli-json/set_wifi_radio", 1, 1, lf_tools.two_radios[i], 1)
            time.sleep(0.5)
            lf_test.Client_Connect_Using_Radio(ssid=ssid_name, passkey=profile_data["security_key"], radio=lf_tools.two_radios[i], station_name=sta[i])
            time.sleep(0.5)
        for i in range(4):
            lf_tests.attenuator_modify(3022, i, 100)
            time.sleep(0.5)
        for i in range(2):
            lf_tests.attenuator_modify(3025, i, 400)
            time.sleep(0.5)

        #lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="tcp_upload_short_med_dis_nss1_2g", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="3,6",
                                        upload_rate="4Mbps", protocol="TCP-IPv4", duration="120000", create_stations=False)


        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True