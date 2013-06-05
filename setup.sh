DIR_LOCATION='/Users/johndebovis/workspace/osx-usages-stats'

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

# sudo chown root $DIR_LOCATION/misc
# sudo chown root adbind.bash
# sudo chmod 755 adbind.bash
# sudo chown root:wheel com.xxxx.adbind.plist
# sudo chmod 755 com.xxxx.adbind.plist