async def AddSecNASHeader(self, innerObj):
    Obj = NagoreNAS('NASSecHeader')
    SecHdr = 4 if innerObj.PycrateObj._name == '5GMMSecurityModeComplete' else 2
    Obj.set(['5GMMHeaderSec', 'SecHdr'], SecHdr)
