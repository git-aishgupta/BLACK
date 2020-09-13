class PartDetails:
    # getter - get value to populate in query to send to neo4j
    # setter - set value is response Data object

    def get_category(self):
        return self.category

    def get_radius(self):
        return self.radius

    def get_title(self):
        return self.title

    def get_reference(self):
        return self.reference

    def set_category(self, category):
        self.category = category

    def set_radius(self, radius):
        self.radius = radius

    def set_title(self, title):
        self.title = title

    def set_reference(self, reference):
        self.reference = reference
