"""

    Performance Test: Throughput  Across Bandwidth Test: VLAN Mode
    pytest -m "throughput_across_bw_test and VLAN"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.throughput_across_bw_test, pytest.mark.vlan]

raw_lines = [['pkts: 60;142;256;512;1024;MTU;4000'], ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ['bandw_options: %s' % 20],
                     ["show_3s: 1"], ["show_ll_graphs: 1"], ["show_log: 1"]]

setup_params_general_20Mhz = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"],
             "security_key": "something"}]},
    "rf": {
        "is5GHz": {"channelBandwidth": "is20MHz"},
        "is5GHzL": {"channelBandwidth": "is20MHz"},
        "is5GHzU": {"channelBandwidth": "is20MHz"}},
    "radius": False
}


@allure.feature("VLAN MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_20Mhz],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestThroughputAcrossBw20MhzVLAN(object):
    """Throughput Across Bw VLAN Mode
       pytest -m "throughput_across_bw_test and VLAN"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2556", name="WIFI-2556")
    @pytest.mark.bw20Mhz
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_client_wpa2_personal_2g(self, lf_test, lf_tools, station_names_twog, create_lanforge_chamberview_dut,
                                     get_configuration):
        """Throughput Across Bw VLAN Mode
           pytest -m "throughput_across_bw_test and VLAN and wpa2_personal and twog"
        """
        profile_data = setup_params_general_20Mhz["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan = 100
        global raw_lines
        dut_name = create_lanforge_chamberview_dut
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_2G",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2556", name="WIFI-2556")
    @pytest.mark.bw20Mhz
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_client_wpa2_personal_5g(self, lf_test, lf_tools, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):
        """Throughput Across Bw VLAN Mode
           pytest -m "throughput_across_bw_test and VLAN and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general_40Mhz["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = 100
        global raw_lines
        dut_name = create_lanforge_chamberview_dut
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False


setup_params_general_40Mhz = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"],
             "security_key": "something"}]},
    "rf": {
        "is5GHz": {"channelBandwidth": "is40MHz"},
        "is5GHzL": {"channelBandwidth": "is40MHz"},
        "is5GHzU": {"channelBandwidth": "is40MHz"}},
    "radius": False
}


@allure.feature("VLAN MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_40Mhz],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestThroughputAcrossBw40MhzVLAN(object):
    """Throughput Across Bw VLAN Mode
       pytest -m "throughput_across_bw_test and VLAN"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2557", name="WIFI-2557")
    @pytest.mark.bw40Mhz
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_client_wpa2_personal_2g(self, lf_test, lf_tools, station_names_twog, create_lanforge_chamberview_dut,
                                     get_configuration):
        """Throughput Across Bw VLAN Mode
           pytest -m "throughput_across_bw_test and VLAN and wpa2_personal and twog"
        """
        profile_data = setup_params_general_80Mhz["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan = 100
        global raw_lines
        raw_lines[3] = ['bandw_options: %s' % 40]
        dut_name = create_lanforge_chamberview_dut
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_2G",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2557", name="WIFI-2557")
    @pytest.mark.bw40Mhz
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_client_wpa2_personal_5g(self, 
                                     lf_test, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):
        """Throughput Across Bw VLAN Mode
           pytest -m "throughput_across_bw_test and VLAN and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general_80Mhz["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = 100
        global raw_lines
        raw_lines[3] = ['bandw_options: %s' % 40]
        dut_name = create_lanforge_chamberview_dut
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False

setup_params_general_80Mhz = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"],
             "security_key": "something"}]},
    "rf": {
        "is5GHz": {"channelBandwidth": "is80MHz"},
        "is5GHzL": {"channelBandwidth": "is80MHz"},
        "is5GHzU": {"channelBandwidth": "is80MHz"}},
    "radius": False
}


@allure.feature("VLAN MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_80Mhz],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestThroughputAcrossBw80MhzVLAN(object):
    """Throughput Across Bw VLAN Mode
       pytest -m "throughput_across_bw_test and VLAN"
    """
    # @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2558", name="WIFI-2558")
    # @pytest.mark.bw80Mhz
    # @pytest.mark.wpa2_personal
    # @pytest.mark.twog
    # def test_client_wpa2_personal_2g(self,
    #                                  lf_test, station_names_twog, create_lanforge_chamberview_dut,
    #                                  get_configuration):
    #     """Throughput Across Bw VLAN Mode
    #        pytest -m "throughput_across_bw_test and VLAN and wpa2_personal and twog"
    #     """
    #     profile_data = setup_params_general_80Mhz["ssid_modes"]["wpa2_personal"][0]
    #     ssid_name = profile_data["ssid_name"]
    #     security_key = profile_data["security_key"]
    #     security = "open"
    #     mode = "VLAN"
    #     band = "twog"
    #     vlan = 100
    #     dut_name = create_lanforge_chamberview_dut
    #     station = lf_test.Client_Connect(ssid=ssid_name, security=security,
    #                                      passkey=security_key, mode=mode, band=band,
    #                                      station_name=station_names_twog, vlan_id=vlan)
    #
    #     if station:
    #         dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
    #                                    instance_name="TIP_PERF_DPT_WPA2_2G",
    #                                    vlan_id=vlan, dut_name=dut_name, bw="80")
    #         report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
    #         entries = os.listdir("../reports/" + report_name + '/')
    #         pdf = False
    #         for i in entries:
    #             if ".pdf" in i:
    #                 pdf = i
    #         if pdf:
    #             allure.attach.file(source="../reports/" + report_name + "/" + pdf,
    #                                name=get_configuration["access_point"][0]["model"] + "_dataplane")
    #         print("Test Completed... Cleaning up Stations")
    #         lf_test.Client_disconnect(station_name=station_names_twog)
    #         assert station
    #     else:
    #         assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2558", name="WIFI-2558")
    @pytest.mark.bw80Mhz
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_client_wpa2_personal_5g(self, lf_test, lf_tools, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):
        """Throughput Across Bw VLAN Mode
           pytest -m "throughput_across_bw_test and VLAN and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general_80Mhz["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = 100
        global raw_lines
        raw_lines[3] = ['bandw_options: %s' % 80]
        dut_name = create_lanforge_chamberview_dut
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_PERF_DPT_WPA2_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            lf_tools.attach_report_graphs(report_name=report_name)
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False
