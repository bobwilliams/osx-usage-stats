DIR_LOCATION='/Users/bob/workspace/osx-usage-stats'

sudo chown root $DIR_LOCATION/misc/com.sparcedge.memory_stats.plist
sudo launchctl unload $DIR_LOCATION/misc/com.sparcedge.memory_stats.plist
sudo launchctl load $DIR_LOCATION/misc/com.sparcedge.memory_stats.plist
sudo launchctl start com.sparcedge.memory_stats
sudo launchctl list | grep com.sparcedge.memory_stats

sudo chown root $DIR_LOCATION/misc/com.sparcedge.ws_monitor.plist
sudo launchctl unload $DIR_LOCATION/misc/com.sparcedge.ws_monitor.plist
sudo launchctl load $DIR_LOCATION/misc/com.sparcedge.ws_monitor.plist
sudo launchctl start com.sparcedge.ws_monitor
sudo launchctl list | grep com.sparcedge.ws_monitor