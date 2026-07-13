def create_dns_server_tests(agent_list):
    tests = [
            {
            "interval": 900,
            "bgpMeasurements": True,
            "usePublicBgp": True,
            "liveShare": False,
            "testName": "drive.google.com - DNS11",
            "savedEvent": False,
            "type": "dns-server",
            "alertsEnabled": True,
            "enabled": True,
            "bandwidthMeasurements": False,
            "dnsQueryClass": "in",
            "domain": "drive.google.com A",
            "ipv6Policy": "use-agent-policy",
            "mtuMeasurements": True,
            "numPathTraces": 1,
            "pathTraceMode": "classic",
            "probeMode": "auto",
            "networkMeasurements": True,
            "randomizedStartTime": False,
            "recursiveQueries": False,
            "dnsServers": [
                
                   "ns1.google.com.","ns2.google.com.","ns3.google.com.","ns4.google.com."
                
            ],
            "agents": [{"agentId": "4739"}]
            },
            {
            "interval": 900,
            "bgpMeasurements": True,
            "usePublicBgp": True,
            "liveShare": False,
            "testName": "elisa.fi - DNS11",
            "savedEvent": False,
            "type": "dns-server",
            "alertsEnabled": True,
            "enabled": True,
            "bandwidthMeasurements": False,
            "dnsQueryClass": "in",
            "domain": "elisa.fi A",
            "ipv6Policy": "use-agent-policy",
            "mtuMeasurements": True,
            "numPathTraces": 1,
            "pathTraceMode": "classic",
            "probeMode": "auto",
            "networkMeasurements": True,
            "randomizedStartTime": False,
            "recursiveQueries": False,
            "dnsServers": [
                
                   "193.229.0.40",
                "193.229.0.42"
                
            ],
           "agents": [{"agentId": "4739"}]
            },
            {
            "interval": 900,
            "bgpMeasurements": True,
            "usePublicBgp": True,
            "liveShare": False,
            "testName": "GMail Basic Mail DNS11",
            "savedEvent": False,
            "type": "dns-server",
            "alertsEnabled": True,
            "enabled": True,
            "bandwidthMeasurements": False,
            "dnsQueryClass": "in",
            "domain": "mail.google.com A",
            "ipv6Policy": "use-agent-policy",
            "mtuMeasurements": True,
            "numPathTraces": 1,
            "pathTraceMode": "classic",
            "probeMode": "auto",
            "networkMeasurements": True,
            "randomizedStartTime": False,
            "recursiveQueries": False,
            "dnsServers": [
                "193.229.0.40",
                "193.229.0.42"
                
            ],
            "agents": [{"agentId": "4739"}]
            },
            {
            "interval": 900,
            "bgpMeasurements": True,
            "usePublicBgp": True,
            "liveShare": False,
            "testName": "Google Meet Basic - DNS11",
            "savedEvent": False,
            "type": "dns-server",
            "alertsEnabled": True,
            "enabled": True,
            "bandwidthMeasurements": False,
            "dnsQueryClass": "in",
            "domain": "meet.google.com A",
            "ipv6Policy": "use-agent-policy",
            "mtuMeasurements": True,
            "numPathTraces": 1,
            "pathTraceMode": "classic",
            "probeMode": "auto",
            "networkMeasurements": True,
            "randomizedStartTime": False,
            "recursiveQueries": False,
            "dnsServers": [
                "193.229.0.40",
                "193.229.0.42"
                
            ],
            "agents": [{"agentId": "4739"}]
            }
            ]
    return tests