import daemon
import dbDaemon
with daemon.DaemonContext():
    dbDaemon.run()
