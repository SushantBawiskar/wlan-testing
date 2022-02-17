"""

    Performance Test: Dataplane Throughput Test: BRIDGE Mode
    pytest -m "dataplane_throughput_test and BRIDGE"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.performance, pytest.mark.dataplane_throughput_test,
              pytest.mark.bridge]  # , pytest.mark.usefixtures("setup_test_run")]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@allure.suite("performance")
@allure.feature("BRIDGE MODE Dataplane Throughput Test")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestDataplaneThroughputBRIDGE(object):
    """
    Dataplane THroughput BRIDGE Mode
    pytest -m "dataplane_throughput_test and BRIDGE"
    """
    @pytest.mark.nikita
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.twow
    def test_tcp_upd_wpa2_personal_bridge_5g_band_ac_station(self, lf_tools,
                                                             lf_test, station_names_fiveg,
                                                             create_lanforge_chamberview_dut,
                                                             get_configuration):
        """Dataplane THroughput BRIDGE Mode
           pytest -m "dataplane_throughput_test and BRIDGE and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut

        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_DPT_DPT_WPA2_2G_BRIDGE",
                                       vlan_id=vlan, dut_name=dut_name)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Dataplane Throughput Test - TCP-UDP 2.4G")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False
