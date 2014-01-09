# boot.py

import sys

class RollbackImporter:
    def __init__(self):
        "Creates an instance and installs as the global importer"
        self.previousModules = sys.modules.copy()

    def uninstall(self):
        newmodules = sys.modules.copy()
        for modname in newmodules.keys():
            if modname not in self.previousModules and modname != "boot":
                # Force reload when modname next imported
                #print("Unloading '%s'" % modname)
                # force delete module globals
                for v in sys.modules[modname].__dict__.copy():
                    if v.startswith("__"):
                        continue
                    del sys.modules[modname].__dict__[v]
                del sys.modules[modname]

def main():
    #print(sys.path)
    if "/c/py" not in sys.path:
        sys.path.insert(0, "/c/py")
    if "." not in sys.path:
        sys.path.insert(0, ".")

    import traceback
    import gc
    import time
    #import runpy
    print("Importing runner")
    from RobotLib import runner
    print("runner imported")

    while True:
        rollback = RollbackImporter()
        robot = None
        try:
            #print("Importing user code.")
            #robot = __import__("robot")
            print("Running user code.")
            #robot.run()
            runner.run()
            #runpy.run_module("robot", run_name="__main__")
        except SystemExit as e:
            print("User code raised SystemExit", str(e))
        except:
            print("Exception in user code.")
            print("-"*60)
            traceback.print_exc(file=sys.stdout)
            print("-"*60)
        else:
            print("Robot program terminated normally")

        # The following code doesn't work to restart the program.  It doesn't
        # re-initialize the socket module properly.  So we'll punt back to the
        # FRC_UserProgram and let it do the restart.
        raise SystemRestart

        print("Waiting 5 seconds before restart...")
        time.sleep(5)
        sys.exc_traceback = None
        sys.last_traceback = None
        rollback.uninstall()
        if robot is not None:
            del robot
            robot = None
        gc.collect()

if __name__ == "__main__":
    main()

