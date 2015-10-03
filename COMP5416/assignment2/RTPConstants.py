import Tkconstants

N=Tkconstants.N
W=Tkconstants.W
E=Tkconstants.E
S=Tkconstants.S

class Cstate:
	CONNECTERROR=-1
	INIT=0
	READY=1
	PLAYING=2
class ActionEvents:
	SETUP=0
	PLAY=1
	PAUSE=2
	TEARDOWN=3
	EVSTEPUP="SETUP"
	EVPLAY="PLAY"
	EVPAUSE="PAUSE"
	EVTEARDOWN="TEARDOWN"

RTSPVERSION="RTSP/1.0"
RTPTRANSPORT="RTP/UDP"
RTSPBUFFERSIZE=1024
RTPBUFFERSIZE=20480
RESPONSE_OK="200 OK"
RESPONSE_OK_END="200 OK END"
RESPONSE_NOTFOUND="404 NOTFOUND"