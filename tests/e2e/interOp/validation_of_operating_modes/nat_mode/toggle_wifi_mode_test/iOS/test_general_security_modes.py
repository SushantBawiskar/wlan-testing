from logging import exception
import io
import unittest
import warnings
from perfecto.test import TestResultFactory
import pytest
import sys
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
import random
import string
import sys
import allure

if 'perfecto_libs' not in sys.path:
    sys.path.append(f'../libs/perfecto_libs')

from iOS_lib import closeApp, openApp, get_WifiIPAddress_iOS, ForgetWifiConnection, ping_deftapps_iOS, \
    Toggle_AirplaneMode_iOS, set_APconnMobileDevice_iOS, verify_APconnMobileDevice_iOS, Toggle_WifiMode_iOS, tearDown,\
    verifyUploadDownloadSpeediOS, get_ip_add_ios, get_ip_add_check_ios, wifi_connect, wifi_disconnect_and_forget

pytestmark = [pytest.mark.regression, pytest.mark.interop, pytest.mark.ios, pytest.mark.interop_ios,
              pytest.mark.client_reconnect, pytest.mark.nat, pytest.mark.ToggleWifiMode]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"]},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"]}],
        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["5G"],
                 "security_key": "something"}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"],
             "security_key": "something"}]},
    "rf": {},
    "radius": False
}
for sec_modes in setup_params_general['ssid_modes'].keys():
    for i in range(len(setup_params_general['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)

        setup_params_general['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string


@allure.suite(suite_name="interop sanity")
@allure.sub_suite(sub_suite_name="Nat Mode Client Reconnect : Suite-A")
@pytest.mark.InteropsuiteA
@allure.feature("NAT MODE CLIENT RECONNECT")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestToggleWifiModeSuiteOneNat(object):
    """ Client Connectivity SuiteA
        pytest -m "client_reconnect and nat and InteropsuiteA"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6609", name="WIFI-6609")
    @pytest.mark.fiveg
    @pytest.mark.wpa2_personal
    def test_ToggleWifiMode_5g_WPA2_Personal_NAT(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data,
                                          setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_add_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_iOS(request, setup_perfectoMobile_iOS, connData)
            ip_check, is_internet_check = get_ip_add_check_ios(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_iOS, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6610", name="WIFI-6610")
    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    def test_ToggleWifiMode_2g_WPA2_Personal_NAT(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_add_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_iOS(request, setup_perfectoMobile_iOS, connData)
            ip_check, is_internet_check = get_ip_add_check_ios(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_iOS, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6607", name="WIFI-6607")
    @pytest.mark.fiveg
    @pytest.mark.wpa
    def test_ToggleWifiMode_5g_WPA_NAT(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_add_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_iOS(request, setup_perfectoMobile_iOS, connData)
            ip_check, is_internet_check = get_ip_add_check_ios(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_iOS, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6608", name="WIFI-6608")
    @pytest.mark.twog
    @pytest.mark.wpa
    def test_ToggleWifiMode_2g_WPA_NAT(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_add_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_iOS(request, setup_perfectoMobile_iOS, connData)
            ip_check, is_internet_check = get_ip_add_check_ios(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_iOS, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6613", name="WIFI-6613")
    @pytest.mark.fiveg
    @pytest.mark.open
    def test_ToggleWifiMode_5g_Open_NAT(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = "[BLANK]"
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_add_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_iOS(request, setup_perfectoMobile_iOS, connData)
            ip_check, is_internet_check = get_ip_add_check_ios(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_iOS, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6614", name="WIFI-6614")
    @pytest.mark.twog
    @pytest.mark.open
    def test_ToggleWifiMode_2g_Open_NAT(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = "[BLANK]"
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_add_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_iOS(request, setup_perfectoMobile_iOS, connData)
            ip_check, is_internet_check = get_ip_add_check_ios(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_iOS, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False





setup_params_general_two = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_p_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_5g", "appliedRadios": ["5G"],
             "security_key": "something"}],
        "wpa3_personal_mixed": [
            {"ssid_name": "ssid_wpa3_p_m_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_m_5g", "appliedRadios": ["5G"],
             "security_key": "something"}],
        "wpa_wpa2_personal_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_p_m_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa_wpa2_p_m_5g", "appliedRadios": ["5G"],
             "security_key": "something"}]
    },
    "rf": {},
    "radius": False
}
for sec_modes in setup_params_general_two['ssid_modes'].keys():
    for i in range(len(setup_params_general_two['ssid_modes'][sec_modes])):
        N = 3
        rand_string = (''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N)))+str(int(time.time_ns())%10000)
        setup_params_general_two['ssid_modes'][sec_modes][i]['ssid_name'] = setup_params_general_two['ssid_modes'][sec_modes][i]['ssid_name'] + "_"+ rand_string


@allure.suite(suite_name="interop regression")
@allure.sub_suite(sub_suite_name="NAT Mode Client Reconnect : Suite-B")
@pytest.mark.InteropsuiteB
@allure.feature("NAT MODE CLIENT Reconnect")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestToggleAirplaneModeSuiteNatTwo(object):
    """ Client Connectivity SuiteA
        pytest -m "client_reconnect and bridge and InteropsuiteB"
    """

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6611", name="WIFI-6611")
    @pytest.mark.fiveg
    @pytest.mark.wpa3_personal
    def test_ToggleWifiMode_5g_wpa3_personal_NAT(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_add_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_iOS(request, setup_perfectoMobile_iOS, connData)
            ip_check, is_internet_check = get_ip_add_check_ios(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_iOS, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6612", name="WIFI-6612")
    @pytest.mark.twog
    @pytest.mark.wpa3_personal
    def test_ToggleWifiMode_2g_wpa3_personal_NAT(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_add_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_AirplaneMode_iOS(request, setup_perfectoMobile_iOS, connData)
            ip_check, is_internet_check = get_ip_add_check_ios(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_iOS, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6615", name="WIFI-6615")
    @pytest.mark.fiveg
    @pytest.mark.wpa3_personal_mixed
    def test_ToggleWifiMode_5g_wpa3_personal_mixed_NAT(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal_mixed"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_add_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_iOS(request, setup_perfectoMobile_iOS, connData)
            ip_check, is_internet_check = get_ip_add_check_ios(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_iOS, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6616", name="WIFI-6616")
    @pytest.mark.twog
    @pytest.mark.wpa3_personal_mixed
    def test_ToggleWifiMode_2g_wpa3_personal_mixed_NAT(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal_mixed"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_add_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_iOS(request, setup_perfectoMobile_iOS, connData)
            ip_check, is_internet_check = get_ip_add_check_ios(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_iOS, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6617", name="WIFI-6617")
    @pytest.mark.fiveg
    @pytest.mark.wpa_wpa2_personal_mixed
    def test_ToggleWifiMode_5g_wpa_wpa2_personal_mixed_NAT(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general_two["ssid_modes"]["wpa_wpa2_personal_mixed"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]

        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_add_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_iOS(request, setup_perfectoMobile_iOS, connData)
            ip_check, is_internet_check = get_ip_add_check_ios(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_iOS, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-6618", name="WIFI-6618")
    @pytest.mark.twog
    @pytest.mark.wpa_wpa2_personal_mixed
    def test_ToggleWifiMode_2g_wpa_wpa2_personal_mixed_NAT(self, request, get_vif_state, get_ap_logs, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general_two["ssid_modes"]["wpa_wpa2_personal_mixed"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        # ssidPassword = "[BLANK]"
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_add_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        #
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            # wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_android, connData)
            Toggle_WifiMode_iOS(request, setup_perfectoMobile_iOS, connData)
            ip_check, is_internet_check = get_ip_add_check_ios(request, ssidName, ssidPassword,
                                                               setup_perfectoMobile_iOS, connData)
            if (ip_check == ip):
                assert True
            else:
                assert False
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False