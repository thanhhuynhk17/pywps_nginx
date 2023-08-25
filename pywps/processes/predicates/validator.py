class Validator():
    """Input validator for predicate operators.
    """

    def _handler(self, geomA, geomB):
        from common.helpers import predicate_validator
        from pywps.app.exceptions import ProcessError

        # input validation
        if not predicate_validator(geomA, geomB):
            raise ProcessError(f'A-size{len(geomA)} and B-size{len(geomB)} invalid, \
                    must be n-to-n or n-to-1.')

        return True
