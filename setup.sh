DIR_LOCATION='/Users/johndebovis/workspace/osx-usages-stats'

sudo chown root $DIR_LOCATION/misc/com.sparcedge.memory-stats.plist
sudo launchctl unload $DIR_LOCATION/misc/com.sparcedge.memory-stats.plist
sudo launchctl load $DIR_LOCATION/misc/com.sparcedge.memory-stats.plist
sudo launchctl start com.sparcedge.memory-stats
sudo launchctl list | grep com.sparcedge.memory-stats

sudo chown root $DIR_LOCATION/misc/com.sparcedge.ws_monitor.plist
sudo launchctl unload $DIR_LOCATION/misc/com.sparcedge.ws_monitor.plist
sudo launchctl load $DIR_LOCATION/misc/com.sparcedge.ws_monitor.plist
sudo launchctl start com.sparcedge.ws_monitor
sudo launchctl list | grep com.sparcedge.ws_monitor