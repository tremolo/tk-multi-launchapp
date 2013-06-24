"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------

This file is loaded automatically by Nuke at startup, after init.py.
It sets up the tank context and prepares the Tank Nuke engine.


NOTE!

When opening a new scene in Nuke, Nuke launches a new process.

So a file->new operation is effectively equivalent to starting 
that very first session, again. Meaning that the bootstrap script will
run again. This is not what we want - we only want the bootstrap script
to run the very first time nuke starts. So therefore, we unset the env vars
once the engine has been created. 

"""


import os
import nuke

def bootstrap_tank():

    try:
        import tank
    except Exception, e:
        nuke.warning("Shotgun: Could not import sgtk! Disabling for now: %s" % e)
        return
    
    if not "TANK_ENGINE" in os.environ:
        # key environment missing. This is usually when someone has done a file->new
        # and this menu.py is triggered but the env vars have been removed
        # because the boot strap is handled by the engine's callback system
        # rather than this startup script.
        return
    
    engine_name = os.environ.get("TANK_ENGINE")
    try:
        context = tank.context.deserialize(os.environ.get("TANK_CONTEXT"))
    except Exception, e:
        nuke.warning("Shotgun: Could not create context! Shotgun pipeline toolkit will be disabled. Details: %s" % e)
        return

    try:    
        engine = tank.platform.start_engine(engine_name, context.tank, context)
    except Exception, e:
        nuke.warning("Shotgun: Could not start engine: %s" % e)
        return
    
    # clean up temp env vars
    for var in ["TANK_ENGINE", "TANK_CONTEXT", "TANK_FILE_TO_OPEN"]:
        if var in os.environ:
            del os.environ[var]


bootstrap_tank()
