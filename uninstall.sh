DIR_LOCATION='/Users/bob/workspace/osx-usage-stats'

sudo chown root $DIR_LOCATION/misc/com.sparcedge.memory_stats.plist
sudo launchctl stop com.sparcedge.memory_stats
sudo launchctl unload $DIR_LOCATION/misc/com.sparcedge.memory_stats.plist

sudo chown root $DIR_LOCATION/misc/com.sparcedge.ws_monitor.plist
sudo launchctl stop com.sparcedge.ws_monitor
sudo launchctl unload $DIR_LOCATION/misc/com.sparcedge.ws_monitor.plist
