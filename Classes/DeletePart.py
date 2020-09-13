from flask import request
import json

from Classes.PartDetails import PartDetails


class DeletePart:
    def partDeletion(self):
        req_data = request.get_json()
        partDetails = PartDetails()
        pd = req_data["data"]["partDetails"]
        reference = pd["title"]
        partDetails.set_reference(reference)
        partDetails.set_radius(reference)
        partDetails.set_title(reference)
        return partDetails.__dict__
