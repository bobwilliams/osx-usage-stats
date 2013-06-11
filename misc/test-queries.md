Test Queries for TurbineDB
--------------------------

## Inserts

New wake notification event:

    http://localhost:8080/db/usagestats/nsworkspace -d '{"timestamp": 1364134494335, "data": {"NOTIFICATION_CONTEXT": "NSWorkspace Notification NSWorkspaceDidWakeNotification", "NOTIFICATION_KEY": "NSWorkspaceDidWakeNotification"}}''

New reminders launch notification event:

    http://localhost:8080/db/usagestats/nsworkspace -d '{"timestamp": 1364135516840, "data": {"NSAPPLICATION_NAME": "Reminders", "NSAPPLICATION_PROCESS_SERIAL_NUMBER_HIGH": "0", "NSAPPLICATION_PROCESS_IDENTIFIER": "79648", "NSWORKSPACE_APPLICATION_KEY": "<NSRunningApplication: 0x7bba6910 (com.apple.reminders - 79648)>", "NOTIFICATION_KEY": "NSWorkspaceDidLaunchApplicationNotification", "NSAPPLICATION_BUNDLE_IDENTIFIER": "com.apple.reminders", "NSAPPLICATION_PROCESS_SERIAL_NUMBER_LOW": "19829480", "NSAPPLICATION_PATH": "/Applications/Reminders.app", "NOTIFICATION_CONTEXT": "NSWorkspace Notification NSWorkspaceDidLaunchApplicationNotification"}}''


## Selects

Total number of Reminders events:

    http://localhost:8080/db/usagestats/nsworkspace?q={"match" : [{ "NSAPPLICATION_NAME" : {"eq":"Reminders"} }] , "reduce" : [ {"total" : {"count": "NOTIFICATION_KEY"}}]}

Total number of times Reminders has been launched:

    http://localhost:8080/db/usagestats/nsworkspace?q={"match" : [{ "NSAPPLICATION_NAME" : {"eq":"Reminders"}}, {"NOTIFICATION_KEY": {"eq": "NSWorkspaceDidLaunchApplicationNotification" }} ] , "reduce" : [ {"total" : {"count": "NOTIFICATION_KEY"}}]}

Should always return empty because NSWorkspaceDidWakeNotification doesn't have an associated APPLICATION_KEY:

    http://localhost:8080/db/usagestats/nsworkspace?q={"match" : [{ "NOTIFICATION_KEY" : {"eq":"NSWorkspaceDidWakeNotification"} }] , "reduce" : [ {"total" : {"count": "APPLICATION_NAME"}}]}

Total events:

    http://localhost:8080/db/usagestats/nsworkspace?q={"reduce" : [ {"total" : {"count": "NOTIFICATION_KEY"}}]}

Total number of times mba woke from sleep:

    http://localhost:8080/db/usagestats/nsworkspace?q={"match" : [{ "NOTIFICATION_KEY" : {"eq":"NSWorkspaceDidWakeNotification"} }] , "reduce" : [ {"total" : {"count": "NOTIFICATION_KEY"}}]}

Average free memory:

    http://localhost:8080/db/usagestats/memory?q={"reduce" : [ {"avg-free-memory" : {"avg": "MEM_FREE"}}]}

Average free memory by hour:

    http://localhost:8080/db/usagestats/memory?q={"group":[{"duration":"month"}],"reduce" : [ {"avg-free-memory" : {"avg": "MEM_FREE"}}]}

Average for all memory stats:

    http://localhost:8080/db/usagestats/memory?q={"reduce" : [ {"avg-wired" : {"avg": "MEM_WIRED"}} , {"avg-active" : {"avg": "MEM_ACTIVE"}}, {"avg-inactive" : {"avg": "MEM_INACTIVE"}}, {"avg-used" : {"avg": "MEM_USED"}}, {"avg-free" : {"avg": "MEM_FREE"}} ]}

Average for all memory stats by minute:

    http://localhost:8080/db/usagestats/memory?q={"group":[{"duration":"minute"}],"reduce":[{"avg-wired":{"avg":"MEM_WIRED"}},{"avg-active":{"avg":"MEM_ACTIVE"}},{"avg-inactive":{"avg":"MEM_INACTIVE"}},{"avg-used":{"avg":"MEM_USED"}},{"avg-free":{"avg":"MEM_FREE"}}]}
