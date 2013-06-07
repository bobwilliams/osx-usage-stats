DIR_LOCATION='/Users/bob/workspace/osx-usage-stats'

sudo chown root $DIR_LOCATION/misc/com.sparcedge.memory-stats.plist
sudo launchctl stop com.sparcedge.memory-stats
sudo launchctl unload $DIR_LOCATION/misc/com.sparcedge.memory-stats.plist

sudo chown root $DIR_LOCATION/misc/com.sparcedge.ws_monitor.plist
sudo launchctl stop com.sparcedge.ws_monitor
sudo launchctl unload $DIR_LOCATION/misc/com.sparcedge.ws_monitor.plist
