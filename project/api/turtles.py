from ast import literal_eval

from flask import current_app as app, request
from flask_restful import Resource

from project.api.metrics import timing

from project import turtle_manager


class TurtlesList(Resource):

    @timing
    def get(self):
        """
        Get all Turtles
        """
        app.logger.info("Get All Turtles")
        response_object = {
            "status": "success",
            "data": {"turtles": turtle_manager.df_all.to_json()},
            "message": "All turtles",
        }

        return response_object, 200


class TurtlesPeriodYear(Resource):

    @timing
    def get(self):
        """
        Get data by period and year
        """
        period = request.args.get('period', 'M').upper()
        locations = literal_eval(request.args.get('locations', '[]'))
        app.logger.info(f"Get data by {period} and year")
        try:
            return {
                "status": "success",
                "data": {"turtles": turtle_manager.get_count_per_period_and_year(period, locations).to_json()},
                "message": f"data by {period} and year",
            }, 200
        except ValueError as err:
            return {
                "status": "error",
                "data": {"turtles": None},
                "message": f"{err}",
            }, 400

        return {
            "status": "error",
            "data": {"turtles": None},
            "message": "Uncaught server exeception",
        }, 500


class SumYearSeasonVictory(Resource):

    @timing
    def get(self):
        """
        Get data by period and year
        """
        locations = literal_eval(request.args.get('locations', '[]'))
        app.logger.info("Get data by SumYearSeasonVictory")
        try:
            return {
                "status": "success",
                "data": {"turtles": turtle_manager.sum_year_season_victory(locations)},
                "message": "data by SumYearSeasonVictory",
            }, 200
        except ValueError as err:
            return {
                "status": "error",
                "data": {"turtles": None},
                "message": f"{err}",
            }, 400

        return {
            "status": "error",
            "data": {"turtles": None},
            "message": "Uncaught server exeception",
        }, 500


class GetTwoDimensionsPerGenderVictory(Resource):

    @timing
    def get(self):
        """
        get_two_dimensions_per_gender
        """
        locations = literal_eval(request.args.get('locations', '[]'))
        dim1 = request.args.get('dim1', 'Weight')
        dim2 = request.args.get('dim2', 'Annuli')
        app.logger.info(f"Get data by GetTwoDimensionsPerGenderVictory {dim1} {dim2} {locations}")
        try:
            return {
                "status": "success",
                "data": {"turtles": turtle_manager.get_two_dimensions_per_gender_victory(
                    dim1,
                    dim2,
                    locations),
                    "key": "Gender",
                    "x": dim1,
                    "y": dim2, },
                "message": f"data by GetTwoDimensionsPerGenderVictory {dim1} {dim2} {locations}",
            }, 200
        except ValueError as err:
            return {
                "status": "error",
                "data": {"turtles": None},
                "message": f"{err}",
            }, 400

        return {
            "status": "error",
            "data": {"turtles": None},
            "message": "Uncaught server exeception",
        }, 500


class TurtlesPeriodStartToEnd(Resource):

    @timing
    def get(self):
        """
        Get data by period filtered from start to end
        """
        period = request.args.get('period', 'M').upper()
        endDate = request.args.get('endDate', '2012-06-30')
        app.logger.info(f"Get data by {period} and year")
        try:
            return {
                "status": "success",
                "data": {"turtles": turtle_manager.get_periodStart_to_endDate(period, endDate).to_json()},
                "message": f"data by {period} with {endDate} end date",
            }, 200
        except ValueError as err:
            return {
                "status": "error",
                "data": {"turtles": None},
                "message": f"{err}",
            }, 400

        return {
            "status": "error",
            "data": {"turtles": None},
            "message": "Uncaught server exeception",
        }, 500


if __name__ == '__main__':
    # for local testing
    df = turtle_manager.df_all
