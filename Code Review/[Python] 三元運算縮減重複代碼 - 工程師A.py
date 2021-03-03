async def AddSecNASHeader(self, innerObj):
    Obj = NagoreNAS('NASSecHeader')
    if innerObj.PycrateObj._name == '5GMMSecurityModeComplete':
        Obj.set(['5GMMHeaderSec', 'SecHdr'], 4)
    else:
        Obj.set(['5GMMHeaderSec', 'SecHdr'], 2)
