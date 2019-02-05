#Filename: sample19.tcl

# ==========VEHICULAR ADHOC NETWORKS============
# Define options
set val(chan) Channel/WirelessChannel ;# channel type
set val(prop) Propagation/TwoRayGround ;# radio-propagation model
set val(netif1) Phy/WirelessPhy ;# network interface type
set val(netif2) Phy/WirelessPhy ;# network interface type
set val(mac) Mac/802_11 ;# MAC type
set val(ifq) Queue/DropTail/PriQueue ;# interface queue type
set val(ll) LL ;# link layer type
set val(ant) Antenna/OmniAntenna ;# antenna model
set val(ifqlen) 50 ;# max packet in ifq
set val(nn) 46 ;# number of mobilenodes
set val(rp) AODV ;# routing protocol
set val(x) 200 ;# X dimension of topography
set val(y) 200 ;# Y dimension of topography
set val(stop) 10.0 ;# time of simulation end

# Simulator Instance Creation
set ns [new Simulator]

# set up topography object
set topo [new Topography]
$topo load_flatgrid $val(x) $val(y)
# general operational descriptor- storing the hop details in the network
create-god $val(nn)
# For model 'TwoRayGround'

set dist(20m) 4.80696e-07
set dist(26m) 2.84435e-07
set dist(27m) 2.63756e-07
set dist(28m) 2.45253e-07
set dist(25m) 3.07645e-07
set dist(30m) 2.13643e-07
set dist(35m) 1.56962e-07
set dist(50m) 7.69113e-08
set dist(75m) 3.41828e-08
set dist(60m) 5.34106e-08
set dist(70m) 3.92405e-08
# unity gain, omni-directional antennas
# set up the antennas to be centered in the node and 1.5 meters above it
Antenna/OmniAntenna set X_ 0
Antenna/OmniAntenna set Y_ 0
Antenna/OmniAntenna set Z_ 1.5
Antenna/OmniAntenna set Gt_ 1.0
Antenna/OmniAntenna set Gr_ 1.0
# Initialize the SharedMedia interface with parameters to make
# it work like the 914MHz Lucent WaveLAN DSSS radio interface

$val(netif1) set CPThresh_ 10.0
$val(netif1) set CSThresh_ $dist(70m)
$val(netif1) set RXThresh_ $dist(75m)
$val(netif1) set Rb_ 2*1e6
$val(netif1) set Pt_ 0.2818
$val(netif1) set freq_ 914e+6
$val(netif1) set L_ 1.0

$val(netif2) set CPThresh_ 10.0
$val(netif2) set CSThresh_ $dist(75m)
$val(netif2) set RXThresh_ $dist(75m)
$val(netif2) set Rb_ 2*1e6
$val(netif2) set Pt_ 0.2818
$val(netif2) set freq_ 914e+6
$val(netif2) set L_ 1.0
# set up topography object
set topo [new Topography]
$topo load_flatgrid $val(x) $val(y)

# Create God
set god_ [create-god $val(nn)]

set chan_1_ [new $val(chan)]

# configure node

$ns node-config -adhocRouting $val(rp) \
-llType $val(ll) \
-macType $val(mac) \
-ifqType $val(ifq) \
-ifqLen $val(ifqlen) \
-antType $val(ant) \
-propType $val(prop) \
-phyType $val(netif1) \
-topoInstance $topo \
-agentTrace ON \
-routerTrace ON \
-macTrace OFF \
-movementTrace ON \
-channel $chan_1_ \

for {set i 0} {$i < 1 } {incr i} {
set node_($i) [$ns node]
$node_($i) color black

$node_($i) random-motion 0 ;# disable random motion
}
$ns node-config -adhocRouting $val(rp) \
-llType $val(ll) \
-macType $val(mac) \
-ifqType $val(ifq) \
-ifqLen $val(ifqlen) \
-antType $val(ant) \
-propType $val(prop) \
-phyType $val(netif2) \
-topoInstance $topo \
-agentTrace ON \
-routerTrace ON \
-macTrace OFF \
-movementTrace ON \
-channel $chan_1_ \

for {set i 1} {$i < 4 } {incr i} {
set node_($i) [$ns node]
$node_($i) color black

}
