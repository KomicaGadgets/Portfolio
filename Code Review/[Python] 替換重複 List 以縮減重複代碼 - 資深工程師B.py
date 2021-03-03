async def registration_accept(self, Obj):
    logger.debug("Start NAS Registration Accept.")
    Obj.ShowStruct()
    # TODO: get 5g-guti and other useful data
    self.plmn = Obj.get(['GUTI', '5GSID', 'PLMN'])
    self.amf_region_id = Obj.get(['GUTI', '5GSID', 'AMFRegionID'])
    self.amf_set_id = Obj.get(['GUTI', '5GSID', 'AMFSetID'])
    self.amf_pointer = Obj.get(['GUTI', '5GSID', 'AMFPtr'])
    self.fg_tmsi = Obj.get(['GUTI', '5GSID', '5GTMSI'])
    self.trigger_register_accepted()
    logger.debug("End NAS Registration Accept.")
    await self.registration_complete()
