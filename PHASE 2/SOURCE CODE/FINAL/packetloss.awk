#——— Formula ————:
PacketLoss=GeneratedPackets-ReceivedPackets

#——— AWK script Format——–#

The script has the following format:
BEGIN {}
{
content
}
END {}
Begin part comprises of initialization of variable.
Commands in the content part scan every row of trace file only once.
Ex:
if (pattern) {
action;
}
