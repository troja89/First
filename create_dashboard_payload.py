def create_dashboards(test_ids) :
    dashboards=[  
    {
  "title": "Executive Dashboard11",
  "isPrivate": True,
  "widgets": [
    {
      "title": "Microsoft Teams Executive Summary",
      "visualMode": "Half screen",
      "isEmbedded": False,
      "filters": {},
      "type": "Number",
      "numberCards": [
        {
          "description": "Application Health",
          "measure": {
            "type": "MEAN"
          },
          "compareToPreviousValue": True,
          "shouldExcludeAlertSuppressionWindows": False,
          "dataSource": "CLOUD_AND_ENTERPRISE_AGENTS",
          "metricGroup": "HTTP_SERVER",
          "metric": "WEB_AVAILABILITY",
          "filters": {
            #"TEST_LABEL": ["281474976756609"]
            "TEST" : list(test_ids.keys())
            #"TEST": [281474976844368]
          }
        },
        {
          "minScale": 200,
          "maxScale": 500,
          "description": "Application Response Time",
          "measure": {
            "type": "MEAN"
          },
          "compareToPreviousValue": True,
          "shouldExcludeAlertSuppressionWindows": False,
          "dataSource": "CLOUD_AND_ENTERPRISE_AGENTS",
          "metricGroup": "HTTP_SERVER",
          "metric": "WEB_TTFB",
          "filters": {
            #"TEST_LABEL": [
              #"281474976756609"
           # ]
           "TEST" : list(test_ids.keys())
          }
        },
        {
          "minScale": 80,
          "maxScale": 100,
          "description": "Network Experience",
          "measure": {
            "type": "PERCZERO"
          },
          "compareToPreviousValue": True,
          "shouldExcludeAlertSuppressionWindows": False,
          "dataSource": "ALERTS",
          "metricGroup": "ALERTS",
          "metric": "ALERT_COUNT",
          "filters": {
            "ALERT_RULE": []
          }
        }
      ]
    }
  ],
  "description": "",
  "defaultTimespan": {
    "timespanDuration": 86400,
    "duration": 86400
  },
  "isGlobalOverride": False,
  "isMigratedReport": False
    }
    ]
    return dashboards