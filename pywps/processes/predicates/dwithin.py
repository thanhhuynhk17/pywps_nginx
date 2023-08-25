# from pywps import Process, ComplexInput, LiteralInput, Format, LiteralOutput
# from processes.predicates.validator import Validator

# class Dwithin(Process, Validator):
#     """Returns True if the geometries are within a given distance.
#     """
#     def __init__(self):
#         inputs = [ComplexInput('geomA', 'Geometry', [Format('application/gml+xml')]),
#                 ComplexInput('geomB', 'Geometry', [Format('application/gml+xml')]),
#                 LiteralInput('distance', 'Given distance',
#                              abstract='Negative distances always return False.',
#                              data_type='float')
#                 ]
#         outputs = [LiteralOutput('predicate', 'Dwithin result',data_type='string')]

#         super(Dwithin, self).__init__(
#             self._handler,
#             identifier='dwithin',
#             title='Returns True if the geometries are within a given distance.',
#             abstract="""
#             Using this function is more efficient than computing the distance
#             and comparing the result.""",
#             inputs=inputs,
#             outputs=outputs,
#             store_supported=True,
#             status_supported=True
#         )

#     def _handler(self, request, response):
#         distance = float(request.inputs['distance'].data)
#         geomA, geomB = super(Dwithin, self)._handler(request=request)

#         predicate = geomA.within(geomB, align=False)
#         response.outputs['predicate'].data = str(predicate.values)
#         return response