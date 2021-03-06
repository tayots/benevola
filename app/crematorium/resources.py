from flask import request
from flask.ext.restful import Resource, abort, marshal_with, marshal
from app import rest_api
from .fields import *
from .forms import AddCremationForm
from app.home.forms import AddDeceasedForm
from .services import *
from app.utils.response_transformer import merge_two_dicts
import logging

log = logging.getLogger(__name__)


class CrematoriumResource(Resource):
    """
    Resource for Crematorium
    """

    @marshal_with(cremation_complete_fields)
    def get(self):
        """ GET /api/crematorium """
        return get_cremations()

    def post(self):
        """ POST /api/crematorium """
        form_data = request.json
        log.debug('Add Crematorium request: {0}'.format(form_data))
        # dec_form = AddDeceasedForm.from_json(form_data['deceased'])
        # crem_form = AddCremationForm.from_json(form_data)

        # if dec_form.validate() and crem_form.validate():
        crem = create_from_dict(form_data)
        result = dict(status=200, message='OK', cremation=crem)
        return marshal(result, cremation_create_fields)
        # else:
        #     abort(400, message="Invalid Parameters", errors=merge_two_dicts(dec_form.errors, crem_form.errors))


# class CrematoriumDetailResource(Resource):
#     """
#     Resource for Crematorium Detail
#     """
#
#     @marshal_with(section_complete_fields)
#     def get(self, c_id):
#         log.debug('GET Crematorium request id={0}: {1}'.format(c_id, request.json))
#         section = section_service.get_section(c_id)
#         if section:
#             data = section.to_dict()
#             data['blocks'] = section.get_blocks()
#             return data
#         abort(404, message="Crematorium id={0} not found".format(c_id))
#
#     def put(self, c_id):
#         """ PUT /api/crematorium/<c_id> """
#         form_data = request.json
#         log.debug('Update Crematorium request id {0}: {1}'.format(c_id, form_data))
#         form = AddSectionForm.from_json(form_data)
#         if form.validate():
#             try:
#                 section = section_service.update_from_dict(c_id, form_data)
#                 result = dict(status=200, message='OK', section=section)
#                 return marshal(result, section_create_fields)
#             except CrematoriumNotFoundError as err:
#                 abort(404, message=err.message)
#         else:
#             abort(400, message="Invalid Parameters", errors=form.errors)


rest_api.add_resource(CrematoriumResource, '/api/crematorium')
# rest_api.add_resource(CrematoriumDetailResource, '/api/crematorium/<int:c_id>')
