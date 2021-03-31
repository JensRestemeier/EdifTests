import spydrnet as sdn

# create netlist and library
netlist = sdn.Netlist('Minimal')
library = netlist.create_library("Work")

# define elements
and2_def = library.create_definition("AND2")
and2_in_A = and2_def.create_port("A")
and2_in_A.create_pin()
and2_in_A.direction = sdn.Port.Direction.IN
and2_in_B = and2_def.create_port("B")
and2_in_B.create_pin()
and2_in_B.direction = sdn.Port.Direction.IN
and2_out_Q = and2_def.create_port("Q")
and2_out_Q.create_pin()
and2_out_Q.direction = sdn.Port.Direction.OUT

or2_def = library.create_definition("OR2")
or2_in_A = or2_def.create_port("A")
or2_in_A.create_pin()
or2_in_A.direction = sdn.Port.Direction.IN
or2_in_B = or2_def.create_port("B")
or2_in_B.create_pin()
or2_in_B.direction = sdn.Port.Direction.IN
or2_out_Q = or2_def.create_port("Q")
or2_out_Q.create_pin()
or2_out_Q.direction = sdn.Port.Direction.OUT

widget_def = library.create_definition("Widget")
widget_in_A = widget_def.create_port("A")
widget_in_A.create_pin()
widget_in_A.direction = sdn.Port.Direction.IN
widget_in_B = widget_def.create_port("B")
widget_in_B.create_pin()
widget_in_B.direction = sdn.Port.Direction.IN
widget_in_C = widget_def.create_port("C")
widget_in_C.create_pin()
widget_in_C.direction = sdn.Port.Direction.IN
widget_in_D = widget_def.create_port("D")
widget_in_D.create_pin()
widget_in_D.direction = sdn.Port.Direction.IN
widget_out_O = widget_def.create_port("O")
widget_out_O.create_pin()
widget_out_O.direction = sdn.Port.Direction.OUT

instance1 = widget_def.create_child("instance1")
instance1.reference = and2_def
ca1 = widget_def.create_cable("ca1")
w = ca1.create_wire()
w.connect_pin(widget_in_A.pins[0])
w.connect_pin(instance1.pins[and2_in_A.pins[0]])

ca2 = widget_def.create_cable("ca2")
w = ca2.create_wire()
w.connect_pin(widget_in_B.pins[0])
w.connect_pin(instance1.pins[and2_in_B.pins[0]])

instance2 = widget_def.create_child("instance2")
instance2.reference = and2_def

ca3 = widget_def.create_cable("ca3")
w = ca3.create_wire()
w.connect_pin(widget_in_C.pins[0])
w.connect_pin(instance2.pins[and2_in_A.pins[0]])

ca4 = widget_def.create_cable("ca4")
w = ca4.create_wire()
w.connect_pin(widget_in_D.pins[0])
w.connect_pin(instance2.pins[and2_in_B.pins[0]])

instance3 = widget_def.create_child("instance3")
instance3.reference = or2_def

ca5 = widget_def.create_cable("ca5")
w = ca5.create_wire()
w.connect_pin(instance1.pins[and2_out_Q.pins[0]])
w.connect_pin(instance3.pins[or2_in_A.pins[0]])

ca6 = widget_def.create_cable("ca6")
w = ca6.create_wire()
w.connect_pin(instance2.pins[and2_out_Q.pins[0]])
w.connect_pin(instance3.pins[or2_in_B.pins[0]])

ca7 = widget_def.create_cable("ca7")
w = ca7.create_wire()
w.connect_pin(instance3.pins[or2_out_Q.pins[0]])
w.connect_pin(widget_out_O.pins[0])

# Create the top instance
top_instance = sdn.Instance("top")
top_instance.reference = widget_def
netlist.top_instance = top_instance

# quick property test:
edif_properties = {
    "INIT":"64'h7FFF8000FFFE0001",
    "CHIP_PIN_LC":"chip1@2" # https://www.intel.com/content/www/us/en/programmable/support/support-resources/design-software/max_plus-ii/plcassn.html
}
instance3["EDIF.properties"] = [{"identifier":key, "value":value} for key,value in edif_properties.items()]
top_instance["EDIF.properties"] = [{"identifier":key, "value":value} for key,value in edif_properties.items()]
widget_in_A["EDIF.properties"] = [{"identifier":key, "value":value} for key,value in edif_properties.items()]
widget_def["EDIF.properties"] = [{"identifier":key, "value":value} for key,value in edif_properties.items()]
# ... the code seems to only write EDIF.properties from an instance node? https://github.com/byuccl/spydrnet/blob/822f273af6782133d809947ef06dba6d7295dfd3/spydrnet/composers/edif/composer.py#L373

# save to file
netlist.compose('minimal.edf')
