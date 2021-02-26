class StepData:
    # getters
    def get_fileDescription(self):
        return self.fileDescription
    
    def get_filename(self):
        return self.filename
    
    def get_manifoldSolidBrepCount(self):
        return self.manifoldSolidBrepCount
    
    def get_totalPlaneSurfaces(self):
        return self.totalPlaneSurfaces

    def get_radius(self):
        return self.radius

    def get_category(self):
        return self.category

    def get_gdriveFileId(self):
        return self.gdriveFileId

    def get_serialNumber(self):
        return self.serialNumber

    # setters
    def set_fileDescription(self, fileDescription):
        self.fileDescription = fileDescription

    def set_filename(self, filename):
        self.filename = filename
    
    def set_manifoldSolidBrepCount(self, manifoldSolidBrepCount):
        self.manifoldSolidBrepCount = manifoldSolidBrepCount
    
    def set_totalPlaneSurfaces(self, totalPlaneSurfaces):
        self.totalPlaneSurfaces = totalPlaneSurfaces
    
    def set_radius(self, radius):
        self.radius = radius

    def set_category(self, category):
        self.category = category
    
    def set_gdriveFileId(self, gdriveFileId):
        self.gdriveFileId = "https://drive.google.com/file/d/" + gdriveFileId + "/view"
    
    def set_serialNumber(self, serialNumber):
        self.serialNumber = serialNumber