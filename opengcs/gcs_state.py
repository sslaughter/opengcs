# _COMPONENT tag is used to mark any place we need to modify code to add support for multiple components
# TODO catch SerialException when reading serial port
# TODO connecting to a 2nd MAV causes the focus to change to the new mav, when it shouldn't
#
from pymavlink import mavutil
import threading
import xmltodict
import sys, os, fnmatch, time
import platform
import multiprocessing
import urllib2
import pickle
from PyQt4.QtCore import *

SINGLE = 0b01
SWARM = 0b10



class GCSState:

    """
    Root data model item for gcsstation.

    This class contains the state of the gcs, to include lists of connections, mavs,
    and mavlink components, fleet management data, and configuration  data
    """
    def __init__(self):
        # This object contains all data about mavlink connections, MAVs, and their components
        self.mav_network = MAVNetwork()

        # This object contains all application settings
        self.config = GCSConfig()

        # Flag for whether or not to print debug messages
        self.debug = self.config.settings['debug']

        self.focused_object = None
        self.focused_component_id = 0

        # These are signals that other code can subscribe to
        self.on_focus_changed = []

        # Debug object, which sends debug messages whenever signals are fired.
        # Comment out to reduce verbosity.
        if self.debug:
            debugger = StateDebugger(self)

        self.mav_network.on_mav_added.append(self.catch_mav_added)
        self.mav_network.on_mav_removed.append(self.catch_mav_removed)
        # _COMPONENT
        # self.mav_network.on_component_added.append(self.catch_component_added)
        # self.mav_network.on_component_removed.append(self.catch_component_removed)

    def set_focus(self, object, component_id=0):
        """
        Set the UI focus to a specific object (mav or swarm)

        """

        # If these are already selected, do nothing
        if self.focused_object == object and self.focused_component_id == component_id:
            return

        self.focused_object = object
        self.focused_component_id = component_id

        for signal in self.on_focus_changed:
            signal(self.focused_object, self.focused_component_id)


    # _COMPONENT add focus_add_component() and focus_remove_component methods

    def catch_mav_added(self, mav):
        # If this is the first mav on the network, automatically give it focus
        if len((self.mav_network.mavs.keys())) == 1:
            self.set_focus(mav)
        return

    def catch_mav_removed(self, mav):
        # If the mav network signals a mav has been removed from the network,
        # we also need to remove it from the focus group
        if self.focused_object == mav:
            self.set_focus(None)

    def fetch_parameter_help(self):
        # TODO there is a bug (possibly in the urllib library) where the download freezes
        files = []
        for vehicle in ['APMrover2', 'ArduCopter', 'ArduPlane']:
            url = 'http://autotest.diydrones.com/Parameters/%s/apm.pdef.xml' % vehicle
            path = 'data/paramhelp/' + vehicle + '.xml'
            files.append((url, path))
            url = 'http://autotest.diydrones.com/%s-defaults.parm' % vehicle
            path = 'data/paramhelp/' + vehicle + '-defaults.parm'
            files.append((url, path))
        try:
            print files
            child = multiprocessing.Process(target=download_files, args=(files,))
            child.start()
        except Exception as e:
            print(e)


class MAVNetwork:
    """
    This object represents the state of the mav network, including multiple connections,
    multiple mavs per connection, and multiple components per mav. Also, it internally
    routes incoming mavlink traffic through the connections to the appropriate mavs and
    components.

    It sends signals every time the network is modified. Any other code needing information
    about the network state should subscribe to these messages.
    """
    def __init__(self):

        self.connections = []
        self.mavs = {}

        # Create a list with one swarm, representing all mavs
        self.swarms = [Swarm("All MAVs")]

        # These are signals that other code can subscribe to
        self.on_mav_added = []
        self.on_mav_removed = []
        self.on_connection_added = []
        self.on_connection_removed = []
        self.on_component_added = []
        self.on_component_removed = []
        self.on_network_changed = []
        self.on_mavlink_packet = []

    def add_connection(self, connection):
        """
        Register a new connection with the network
        """
        if connection not in self.connections:
            self.connections.append(connection)
            for signal in self.on_connection_added:
                signal()

    def add_mav(self, mav):
        """
        Register a new mav with the network
        """
        if mav not in self.mavs:
            # Add this mav to the dictionary of all mavs
            self.mavs[mav.system_id] = mav
            # Add this mav to swarm 0, which always represents all mavs
            self.swarms[0].add_mav(mav)

            for signal in self.on_mav_added:
                signal(mav)
            for signal in self.on_network_changed:
                signal()

    def remove_connection(self, conn):
        """
        Unregister a connection and all associated mavs from the network
        """
        if conn in self.connections:
            # Remove all mavs associated with this connection
            for mav in self.get_mavs_on_connection(conn):
                self.remove_mav(mav)

            self.connections.remove(conn)
            for signal in self.on_connection_removed:
                signal()
            for signal in self.on_network_changed:
                signal()

    def remove_mav(self, mav):
        """
        Unregister a mav from the network
        """
        deletekey = None

        for mavkey in self.mavs:
            if self.mavs[mavkey] == mav:
                deletekey = mavkey

        if deletekey is None:
            return

        # Remove this mav from the dictionary of all mavs
        del self.mavs[mavkey]
        # Remove this mav from all swarms where it's found
        for swarm in self.swarms:
            swarm.remove_mav(mav)

        for signal in self.on_mav_removed:
            signal()
        for signal in self.on_network_changed:
            signal()

    def get_mavs_on_connection(self, conn):
        mavs = []
        for mavkey in self.mavs:
            if self.mavs[mavkey].conn == conn:
                mavs.append(self.mavs[mavkey])
        return mavs

    def get_mav_ids(self):
        """
        Get a list of system_ids active on the network
        :return: a list of system_id numbers
        """
        return list(self.mavs.keys())

    def route_messages(self, m, conn):
        """
        This method receives mavlink traffic from ALL open connections. It forwards
        messages to the appropriate mav objects, and adds new mavs as they are
        detected. It alsos signals any subscribers.
        """

        system_id = m.get_header().srcSystem

        # If the source system is 0, every MAV processes it
        # TODO I'm not sure if MAVs ever have a source system of 0
        if system_id == 0:
            for mavkey in self.mavs:
                self.mavs[mavkey].process_messages(m)

        # If the source MAV has already been registered, forward the message to that MAV object
        elif system_id in self.mavs:
            self.mavs[system_id].process_messages(m)

        # Otherwise, it's a new MAV and we need to add it
        else:
            newmav = MAV(conn, system_id)
            self.add_mav(newmav)
            newmav.process_messages(m)

        # Forward packet to subscribers
        for signal in self.on_mavlink_packet:
            signal(m)

class Swarm:
    def __init__(self, name="New Swarm", mavs=[], color = '#000000'):
        self.name = name
        self.mavs = mavs
        self.color = color

        # Signals
        self.on_swarm_changed = []

    def add_mav(self, mav):
        """
        Add a mav to this swarm
        """
        if mav not in self.mavs:
            self.mavs.append(mav)
            for signal in self.on_swarm_changed:
                signal()

    def remove_mav(self, mav):
        """
        Remove a mav from this swarm
        """
        if mav in self.mavs:
            self.mavs.remove(mav)
            for signal in self.on_swarm_changed:
                signal()


class MavlinkThread(QThread):
    """
    This class exists to read incoming mavlink messages in a secondary thread.
    Each Connection spawns one of these threads.
    However, all of the GUI updating needs to happen within the primary thread,
    so all this does is send a signal back to the primary thread any time a
    message is received. Those messages are processed by the Connection
    object.
    """
    def __init__(self, conn):
        super(MavlinkThread, self).__init__()
        self.conn = conn
        self.master = conn.master
        self.command_exit = False

    def run(self):

        while self.command_exit is False:
            m = self.master.recv_match(blocking=True)
            if not m:
                return
            if m.get_type() == "BAD_DATA":
                if mavutil.all_printable(m.data):
                    sys.stdout.write(m.data)
                    sys.stdout.flush()
            self.emit(SIGNAL("messageReceived"), m, self.conn)
        print "Returning from thread loop"

    def request_exit(self):
        self.command_exit = True

class Connection:
    """
    Encapsulates a connection via serial, TCP, or UDP ports, etc.
    """
    def __init__(self, state, port, number):
        self.state = state
        self.port = port
        self.number = number
        self.mavs = {}

        # TODO Support UDP/TCP connections
        if port == "UDP" or port == "TCP":
            return

        self.master = mavutil.mavlink_connection(port, baud=number)

        # Run port monitoring on a secondary thread. Any time a mavlink message is received,
        # it signals for the mav_network.process_messages function to handle the message on the
        # primary thread. That function routes the message to the appropriate vehicles.
        self.thread = MavlinkThread(self)
        self.thread.connect(self.thread, SIGNAL("messageReceived"), self.state.mav_network.route_messages)
        self.thread.start()

        self.state.mav_network.add_connection(self)

    def close(self):
        """
        Close the connection
        """
        # TODO shutting down the thread throws exception
        #self.thread.quit()
        self.thread.disconnect()
        self.thread.request_exit()
        time.sleep(0.5)
        self.master.close()

    def get_name(self):
        """
        Return the name of the port.
        """
        return str(self.port)

    def is_port_dead(self):
        """
        Returns whether the connection is alive or dead
        """
        return self.master.portdead


class MAV:
    """
    This class encapsulates a micro air vehicle (MAV), and theoretically represents the
    state of that vehicle at any moment in time. It is the responsibility of this class to
    communicate with the MAV and keep its internal state up to date.

    My vision is to separate serial connections from MAVs, so that one connection can
    have multiple MAVs. Unfortunately pymavlink doesn't work this way... the connection
    and MAV are interwoven in one mavfile object from pymavlink.mavutil. For now I am
    wrapping the mavfile object inside the MAV class, with the hope that we can later
    separate the two. Most of that work will probably be done inside the MAV class and
    Connection class.
    """
    def __init__(self, conn, system_id):
        self.system_id = system_id
        self.conn = conn
        self.master = conn.master
        self.name = "MAV"
        self.color = '#FFFFFF'

        # Properties related to parameters
        self.mav_param_set = set()  # Index numbers of all parameters received
        self.mav_param = {}         # Actual parameter values
        self.mav_param_count = 0    # Total number of parameters aboard flight controller
        self.fetch_one = 0          # ???
        self.param_fetched = False

        # There may be a better way to do this, but this is my solution to get a list of
        # mavlink messages this mav uses.
        # TODO This currently reads a global mavlink dialect variable from mavutil, but
        # it is possible that each device could speak a different dialect.
        self.msg_types = []
        mavlink_map = mavutil.mavlink.mavlink_map
        for key in mavlink_map.keys():
            self.msg_types.append(mavlink_map[key].name)
        self.msg_types.sort()

        # The class exposes a number of events that other code can subscribe to
        self.on_heartbeat = []
        self.on_param_received = []
        self.on_mission_event = []
        self.on_params_initialized = []
        self.on_params_changed = []

    def get_name(self):
        return str(self.system_id) + ": " + self.name

    def process_messages(self, m):
        """
        Process all incoming mavlink packets from the corresponding vehicle, and forward traffic to onboard
        components as necessary.
        """

        mtype = m.get_type()
        #s = " MAV " + str(self.system_id) + ": From (" + str(m.get_header().srcSystem) + ", " + str(m.get_header().srcComponent) + ")"
        #s = s + ", To (" + m.tar
        #print(" MAV ") + str(self.system_id) + ": processing message from " + str(m.get_header().srcSystem) + ", " + str(m.get_header().srcComponent)

        if mtype == "HEARTBEAT":
            if self.param_fetched == False:
                self.param_fetched = True
                self.fetch_all_parameters()


        # DEBUG: temporary code block for debugging
        if mtype == "VFR_HUD":
            self.altitude = mavutil.evaluate_expression("VFR_HUD.alt", self.master.messages)
            self.airspeed = mavutil.evaluate_expression("VFR_HUD.airspeed", self.master.messages)
            self.heading = mavutil.evaluate_expression("VFR_HUD.heading", self.master.messages)
            #print(str(m.get_header().srcSystem) + ": Altitude: " + str(self.altitude))

        if mtype == 'PARAM_VALUE':
            param_id = "%.16s" % m.param_id
            # Note: the xml specifies param_index is a uint16, so -1 in that field will show as 65535
            # We accept both -1 and 65535 as 'unknown index' to future proof us against someday having that
            # xml fixed.
            if m.param_index != -1 and m.param_index != 65535 and m.param_index not in self.mav_param_set:
                added_new_parameter = True
                self.mav_param_set.add(m.param_index)
            else:
                added_new_parameter = False
            if m.param_count != -1:
                 self.mav_param_count = m.param_count
            self.mav_param[str(param_id)] = m.param_value
            if self.fetch_one > 0:
                self.fetch_one -= 1
                print("%s = %f" % (param_id, m.param_value))
            if added_new_parameter and len(self.mav_param_set) == m.param_count:
                print("Received %u parameters" % m.param_count)

               #if self.logdir != None:
                #    self.mav_param.save(os.path.join(self.logdir, self.parm_file), '*', verbose=True)

                for func in self.on_params_initialized:
                    func()

    def fetch_all_parameters(self):
        print("Fetching all parameters for system ") + str(self.system_id)
        self.master.target_system = self.system_id
        self.master.param_fetch_all()
        self.mav_param_set = set()

    def set_parameter(self, param, value):
        if value.startswith('0x'):
            value = int(value, base=16)
        if not param.upper() in self.mav_param:
            print("Unable to find parameter '%s'" % param)
            return
        self.mav_param.mavset(self.master, param.upper(), value, retries=3)


class StateDebugger:
    """
    This class is for debugging signals/slots related to the GCSState and MAVNetwork objects. It is
    essentially a dummy that subscribes to a variety of signals and prints debug messages.
    """
    def __init__(self, state):
        self.state = state
        self.state.on_focus_changed.append(self.catch_focus_changed)
        self.state.mav_network.on_mav_added.append(self.catch_mav_added)
        self.state.mav_network.on_mav_removed.append(self.catch_mav_removed)
        self.state.mav_network.on_connection_added.append(self.catch_connection_added)
        self.state.mav_network.on_connection_removed.append(self.catch_connection_removed)
        self.state.mav_network.on_component_removed.append(self.catch_component_removed)
        self.state.mav_network.on_component_added.append(self.catch_component_added)
        self.state.mav_network.on_network_changed.append(self.catch_network_changed)
        self.state.on_focus_changed.append(self.catch_focus_changed)

    def catch_focus_changed(self, object, component_id):
        print("Signal: GCSState.on_focus_changed, caught by gcs_state.StateDebugger")
        print("New focus: " + str(object))

    def catch_mav_added(self, mav):
        print("Signal: MAVNetwork.on_mav_added, caught by gcs_state.StateDebugger")
        print("New MAV:" + mav.get_name())

    def catch_mav_removed(self):
        print("Signal: MAVNetwork.on_mav_removed, caught by gcs_state.StateDebugger")

    def catch_connection_added(self):
        print("Signal: MAVNetwork.on_connection_added, caught by gcs_state.StateDebugger")

    def catch_connection_removed(self):
        print("Signal: MAVNetwork.on_connection_removed, caught by gcs_state.StateDebugger")

    def catch_component_added(self, conn):
        print("Signal: MAVNetwork.on_component_added, caught by gcs_state.StateDebugger")
        print("New connection:" + conn.port)

    def catch_component_removed(self):
        print("Signal: MAVNetwork.on_component_removed, caught by gcs_state.StateDebugger")

    def catch_network_changed(self):
        print("Signal: MAVNetwork.catch_nework_changed, caught by gcs_state.StateDebugger")

# Everything below this line is included for reference, from mavproxy module_param, although it is not currently used
class ParamState:
    '''this class is separated to make it possible to use the parameter
       functions on a secondary connection'''
    def __init__(self, master, mav_param, logdir, vehicle_name, parm_file):
        self.master = master
        self.mav_param_set = set()
        self.mav_param_count = 0
        self.param_period = mavutil.periodic_event(1)
        self.fetch_one = 0
        self.mav_param = mav_param
        self.logdir = logdir
        self.vehicle_name = vehicle_name
        self.parm_file = parm_file

    def handle_mavlink_packet(self, master, m):
        '''handle an incoming mavlink packet'''
        if m.get_type() == 'PARAM_VALUE':
            param_id = "%.16s" % m.param_id
            # Note: the xml specifies param_index is a uint16, so -1 in that field will show as 65535
            # We accept both -1 and 65535 as 'unknown index' to future proof us against someday having that
            # xml fixed.
            if m.param_index != -1 and m.param_index != 65535 and m.param_index not in self.mav_param_set:
                added_new_parameter = True
                self.mav_param_set.add(m.param_index)
            else:
                added_new_parameter = False
            if m.param_count != -1:
                self.mav_param_count = m.param_count
            self.mav_param[str(param_id)] = m.param_value
            if self.fetch_one > 0:
                self.fetch_one -= 1
                print("%s = %f" % (param_id, m.param_value))
            if added_new_parameter and len(self.mav_param_set) == m.param_count:
                print("Received %u parameters" % m.param_count)
                if self.logdir != None:
                    self.mav_param.save(os.path.join(self.logdir, self.parm_file), '*', verbose=True)

    def fetch_check(self):
        '''check for missing parameters periodically'''
        if self.param_period.trigger():
            if self.master is None:
                return
            if len(self.mav_param_set) == 0:
                self.master.param_fetch_all()
            elif self.mav_param_count != 0 and len(self.mav_param_set) != self.mav_param_count:
                if self.master.time_since('PARAM_VALUE') >= 1:
                    diff = set(range(self.mav_param_count)).difference(self.mav_param_set)
                    count = 0
                    while len(diff) > 0 and count < 10:
                        idx = diff.pop()
                        self.master.param_fetch_one(idx)
                        count += 1

    def param_help_download(self):
        '''download XML files for parameters'''
        import multiprocessing
        files = []
        for vehicle in ['APMrover2', 'ArduCopter', 'ArduPlane']:
            url = 'http://autotest.diydrones.com/Parameters/%s/apm.pdef.xml' % vehicle
            path = 'data/paramhelp/' + vehicle + '.xml'
            files.append((url, path))
            url = 'http://autotest.diydrones.com/%s-defaults.parm' % vehicle
            path = 'data/paramhelp/' + vehicle + '-defaults.parm'
            files.append((url, path))
        try:
            child = multiprocessing.Process(target=download_files, args=(files,))
            child.start()
        except Exception as e:
            print(e)

    def param_help(self, args):
        '''show help on a parameter'''
        if len(args) == 0:
            print("Usage: param help PARAMETER_NAME")
            return
        if self.vehicle_name is None:
            print("Unknown vehicle type")
            return
        path = dot_opengcs("%s.xml" % self.vehicle_name)
        if not os.path.exists(path):
            print("Please run 'param download' first (vehicle_name=%s)" % self.vehicle_name)
            return
        xml = open(path).read()
        from lxml import objectify
        objectify.enable_recursive_str()
        tree = objectify.fromstring(xml)
        htree = {}
        for p in tree.vehicles.parameters.param:
            n = p.get('name').split(':')[1]
            htree[n] = p
        for lib in tree.libraries.parameters:
            for p in lib.param:
                n = p.get('name')
                htree[n] = p
        for h in args:
            if h in htree:
                help = htree[h]
                print("%s: %s\n" % (h, help.get('humanName')))
                print(help.get('documentation'))
                try:
                    vchild = help.getchildren()[0]
                    print("\nValues: ")
                    for v in vchild.value:
                        print("\t%s : %s" % (v.get('code'), str(v)))
                except Exception as e:
                    pass
            else:
                print("Parameter '%s' not found in documentation" % h)

    def handle_command(self, mpstate, args):
        '''handle parameter commands'''
        param_wildcard = "*"
        usage="Usage: param <fetch|set|show|load|preload|forceload|diff|download|help>"
        if len(args) < 1:
            print(usage)
            return
        if args[0] == "fetch":
            if len(args) == 1:
                self.master.param_fetch_all()
                self.mav_param_set = set()
                print("Requested parameter list")
            else:
                for p in self.mav_param.keys():
                    if fnmatch.fnmatch(p, args[1].upper()):
                        self.master.param_fetch_one(p)
                        self.fetch_one += 1
                        print("Requested parameter %s" % p)
        elif args[0] == "save":
            if len(args) < 2:
                print("usage: param save <filename> [wildcard]")
                return
            if len(args) > 2:
                param_wildcard = args[2]
            else:
                param_wildcard = "*"
            self.mav_param.save(args[1], param_wildcard, verbose=True)
        elif args[0] == "diff":
            wildcard = '*'
            if len(args) < 2 or args[1].find('*') != -1:
                if self.vehicle_name is None:
                    print("Unknown vehicle type")
                    return
                filename = dot_opengcs("%s-defaults.parm" % self.vehicle_name)
                if not os.path.exists(filename):
                    print("Please run 'param download' first (vehicle_name=%s)" % self.vehicle_name)
                    return
                if len(args) >= 2:
                    wildcard = args[1]
            else:
                filename = args[1]
                if len(args) == 3:
                    wildcard = args[2]
            print("%-16.16s %12.12s %12.12s" % ('Parameter', 'Defaults', 'Current'))
            self.mav_param.diff(filename, wildcard=wildcard)
        elif args[0] == "set":
            if len(args) < 2:
                print("Usage: param set PARMNAME VALUE")
                return
            if len(args) == 2:
                self.mav_param.show(args[1])
                return
            param = args[1]
            value = args[2]
            if value.startswith('0x'):
                value = int(value, base=16)
            if not param.upper() in self.mav_param:
                print("Unable to find parameter '%s'" % param)
                return
            self.mav_param.mavset(self.master, param.upper(), value, retries=3)

            #if (param.upper() == "WP_LOITER_RAD" or param.upper() == "LAND_BREAK_PATH"):
            #    #need to redraw rally points
            #    mpstate.module('rally').rallyloader.last_change = time.time()
            #    #need to redraw loiter points
            #    mpstate.module('wp').wploader.last_change = time.time()

        elif args[0] == "load":
            if len(args) < 2:
                print("Usage: param load <filename> [wildcard]")
                return
            if len(args) > 2:
                param_wildcard = args[2]
            else:
                param_wildcard = "*"
            self.mav_param.load(args[1], param_wildcard, self.master)
        elif args[0] == "preload":
            if len(args) < 2:
                print("Usage: param preload <filename>")
                return
            self.mav_param.load(args[1])
        elif args[0] == "forceload":
            if len(args) < 2:
                print("Usage: param forceload <filename> [wildcard]")
                return
            if len(args) > 2:
                param_wildcard = args[2]
            else:
                param_wildcard = "*"
            self.mav_param.load(args[1], param_wildcard, self.master, check=False)
        elif args[0] == "download":
            self.param_help_download()
        elif args[0] == "help":
            self.param_help(args[1:])
        elif args[0] == "show":
            if len(args) > 1:
                pattern = args[1]
            else:
                pattern = "*"
            self.mav_param.show(pattern)
        else:
            print(usage)

class GCSConfig:
    def __init__(self):
        self.settings = {}
        self.perspective = {}
        self.load_settings()


    def load_settings(self):
        """
        Load application configuration from an XML file
        """
        with open('settings.xml') as fd:
            self.settings = xmltodict.parse(fd.read())['settings']
        return

    def save_settings(self):
        """
        Save application configuration to an XML file
        """
        # TODO implement save opengcs settings
        return

def dot_opengcs(name):
    '''return a path to store mavproxy data'''
    # Taken from mavproxy mp_util.py
    dir = os.path.join(os.environ['HOME'], '.opengcs')
    mkdir_p(dir)
    return os.path.join(dir, name)

def mkdir_p(dir):
    '''like mkdir -p'''
    # Taken from mavproxy mp_util.py
    if not dir:
        return
    if dir.endswith("/") or dir.endswith("\\"):
        mkdir_p(dir[:-1])
        return
    if os.path.isdir(dir):
        return
    mkdir_p(os.path.dirname(dir))
    try:
        os.mkdir(dir)
    except Exception:
        pass


# TODO: bug in this code block. The urllib2.urlopen call hangs forever
def download_url(url):
    '''download a URL and return the content'''
    # Taken from mavproxy mp_util.py
    try:
        print(url)
        #resp = urllib2.urlopen(url)
        resp = None

        resp = urllib2.urlopen(url, None, 3)
        print("DEBUG url open")
        headers = resp.info()
        print("DEBUG download_url end try block")
    except urllib2.URLError as e:
        print('Error downloading %s' % url)
        return None
    return resp.read()


def download_files(files):
    '''download an array of files'''
    # Taken from mavproxy mp_util.py
    for (url, file) in files:
        print("Downloading %s as %s" % (url, file))
        data = download_url(url)
        if data is None:
            continue
        try:
            open(file, mode='w').write(data)
        except Exception as e:
            print("Failed to save to %s : %s" % (file, e))

if __name__ == "__main__":
    mav1 = MAV()
    mav1.connect('/dev/tty.usbmodemfa141',115200)
    print("Connected")
    i = 0
    while 0 < 1:
        i = 1 - i




