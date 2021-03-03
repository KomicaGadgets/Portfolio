async def registration_accept(self, Obj):
    logger.debug("Start NAS Registration Accept.")
    Obj.ShowStruct()
    # TODO: get 5g-guti and other useful data
    PrefixList = ['GUTI', '5GSID']
    self.plmn = Obj.get(PrefixList+['PLMN'])
    self.amf_region_id = Obj.get(PrefixList+['AMFRegionID'])
    self.amf_set_id = Obj.get(PrefixList+['AMFSetID'])
    self.amf_pointer = Obj.get(PrefixList+['AMFPtr'])
    self.fg_tmsi = Obj.get(PrefixList+['5GTMSI'])
    self.trigger_register_accepted()
    logger.debug("End NAS Registration Accept.")
    await self.registration_complete()
