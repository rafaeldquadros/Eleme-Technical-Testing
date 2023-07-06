from calls.model import CallsModel


class CallsServices:
    def find_by_id(self, id):
        call = CallsModel.find_by_id(id)
        return call

    def find_all(self):
        calls = CallsModel.find_all()
        return [p.as_dict() for p in calls]

    def create(self, **kwargs):
        new_call = CallsModel(**kwargs)
        new_call.save()
        return new_call.as_dict()

    def delete(self, id):
        call = CallsModel.find_by_id(id)
        if call:
            call.delete(id)
            return {"message": "Call deleted successfully"}
        else:
            return {"error": "Call not found"}, 404

    def update(self, id, **kwargs):
        call = CallsModel.update(id, **kwargs)
        if not call:
            return {"error": "Call not found"}, 404
        else:
            return call
