#!/usr/bin/python2.7
# encoding: utf-8

"""
Monitor system event notifications and log to TurbineDB (http://turbinedb.com)
Largely based off crankd.py found in https://code.google.com/p/pymacadmin/
If running python2.5, this requires simplejson
"""

from Cocoa import \
    CFAbsoluteTimeGetCurrent, \
    CFRunLoopAddSource, \
    CFRunLoopAddTimer, \
    CFRunLoopTimerCreate, \
    NSObject, \
    NSRunLoop, \
    NSWorkspace, \
    kCFRunLoopCommonModes

import logging
import re
from PyObjCTools import AppHelper
from functools import partial
from datetime import datetime
import time
import urllib2
import notify

class BaseHandler(object):
    # pylint: disable-msg=C0111,R0903
    pass

class NSNotificationHandler(NSObject):
    """Simple base class for handling NSNotification events"""
    # Method names and class structure are dictated by Cocoa & PyObjC, which
    # is substantially different from PEP-8:
    # pylint: disable-msg=C0103,W0232,R0903

    def init(self):
        """NSObject-compatible initializer"""
        self = super(NSNotificationHandler, self).init()
        if self is None: return None
        self.callable = self.not_implemented
        return self # NOTE: Unlike Python, NSObject's init() must return self!
    
    def not_implemented(self, *args, **kwargs):
        """A dummy function which exists only to catch configuration errors"""
        # TODO: Is there a better way to report the caller's location?
        import inspect
        stack = inspect.stack()
        my_name = stack[0][3]
        caller  = stack[1][3]
        raise NotImplementedError(
            "%s should have been overridden. Called by %s as: %s(%s)" % (
                my_name,
                caller,
                my_name,
                ", ".join(map(repr, args) + [ "%s=%s" % (k, repr(v)) for k,v in kwargs.items() ])
            )
        )

    def onNotification_(self, the_notification):
        """Pass an NSNotifications to our handler"""
        if the_notification.userInfo:
            user_info = the_notification.userInfo()
        else:
            user_info = None
        self.callable(user_info=user_info) # pylint: disable-msg=E1101

def get_callable_for_event(notification, context=None):
    kwargs = {
        'context':  context,
        'key':      notification
    }

    f = partial(log_event, notification, **kwargs)

    return f

def load_workspace_notifications():
    notification_list = [
        'NSWorkspaceDidLaunchApplicationNotification',
        'NSWorkspaceDidMountNotification',
        'NSWorkspaceDidPerformFileOperationNotification',
        'NSWorkspaceDidTerminateApplicationNotification',
        'NSWorkspaceDidUnmountNotification',
        'NSWorkspaceDidWakeNotification',
        'NSWorkspaceSessionDidBecomeActiveNotification',
        'NSWorkspaceSessionDidResignActiveNotification',
        'NSWorkspaceWillLaunchApplicationNotification',
        'NSWorkspaceWillPowerOffNotification',
        'NSWorkspaceWillSleepNotification',
        'NSWorkspaceWillUnmountNotification'
    ]

    print "Loading the following NSWorkspace Notifications:"

    for notification in notification_list:
        print ">>> " + notification

    return notification_list    

def add_workspace_notifications(notification_list):
    notification_center = NSWorkspace.sharedWorkspace().notificationCenter()

    for notification in notification_list:
        handler          = NSNotificationHandler.new()
        handler.name     = "NSWorkspace Notification %s" % notification
        handler.callable = get_callable_for_event(notification, context=handler.name)

        assert(callable(handler.onNotification_))

        notification_center.addObserver_selector_name_object_(handler, "onNotification:", notification, None)

def timer_callback(*args):
    """Handles the timer events which we use simply to have the runloop run regularly. Currently this logs a timestamp for debugging purposes"""
    logging.debug("timer callback at %s" % datetime.now())

def main():
    add_workspace_notifications(load_workspace_notifications())

    # NOTE: This timer is basically a kludge around the fact that we can't reliably get
    #       signals or Control-C inside a runloop. This wakes us up often enough to
    #       appear tolerably responsive:
    CFRunLoopAddTimer(
        NSRunLoop.currentRunLoop().getCFRunLoop(),
        CFRunLoopTimerCreate(None, CFAbsoluteTimeGetCurrent(), 2.0, 0, 0, timer_callback, None),
        kCFRunLoopCommonModes
    )

    try:
        AppHelper.runConsoleEventLoop(installInterrupt=True)
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt received, exiting")

    sys.exit(0)

def create_env_name(name):
    """
    Converts input names into more traditional shell environment name style

    >>> create_env_name("NSApplicationBundleIdentifier")
    'NSAPPLICATION_BUNDLE_IDENTIFIER'
    >>> create_env_name("NSApplicationBundleIdentifier-1234$foobar!")
    'NSAPPLICATION_BUNDLE_IDENTIFIER_1234_FOOBAR'
    """
    new_name = re.sub(r'''(?<=[a-z])([A-Z])''', '_\\1', name)
    new_name = re.sub(r'\W+', '_', new_name)
    new_name = re.sub(r'_{2,}', '_', new_name)
    return new_name.upper().strip("_")

def log_event(notification, context=None, **kwargs):
    """Executes a shell command with logging"""

    child_env = {'NOTIFICATION_CONTEXT': context}

    # We'll pull a subset of the available information in for shell scripts.
    # Anyone who needs more will probably want to write a Python handler
    # instead so they can reuse things like our logger & config info and avoid
    # ordeals like associative arrays in Bash
    for k in [ 'info', 'key' ]:
        if k in kwargs and kwargs[k]:
            child_env['NOTIFICATION_%s' % k.upper()] = str(kwargs[k])

    user_info = kwargs.get("user_info")
    if user_info:
        for k, v in user_info.items():
            child_env[create_env_name(k)] = str(v)

    """
        Call our changes
    """
    notify.post(child_env)

if __name__ == '__main__':
    main()
