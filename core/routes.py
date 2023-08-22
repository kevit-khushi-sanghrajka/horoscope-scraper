from core import api
from flask import jsonify
from core.utils import get_horoscope_by_day, get_horoscope_by_month, get_horoscope_by_week
from flask_restx import reqparse, Resource
import datetime
from werkzeug.exceptions import BadRequest, NotFound

ZODIAC_SIGNS = {
    "Aries": 1,
    "Taurus": 2,
    "Gemini": 3,
    "Cancer": 4,
    "Leo": 5,
    "Virgo": 6,
    "Libra": 7,
    "Scorpio": 8,
    "Sagittarius": 9,
    "Capricorn": 10,
    "Aquarius": 11,
    "Pisces": 12
}

ns = api.namespace('/', description = 'Horoscope APIs')

parser = reqparse.RequestParser()
parser.add_argument('sign', type=str, required = True)

parser_copy = parser.copy()
parser_copy.add_argument('day', type=str, required = True)

#This kind of approach can be useful in scenarios where you have a common set of arguments 
#that you want to reuse for multiple endpoints, but you need to add 
#or modify arguments for specific endpoints. 

#The parser_copy will not only contain day, but also sign. 
#That is what we'll require for the daily horoscope.

@ns.route('/get-horoscope/daily')
class DailyHoroscopeAPI(Resource):
        @ns.doc(parser=parser_copy)
        def get(self):
                args = parser_copy.parse_args()
                day = args.get('day')
                zodiac_sign = args.get('sign')
                try:
                        zodiac_num = ZODIAC_SIGNS[zodiac_sign.capitalize()]
                        if "-" in day:
                                datetime.strptime(day, '%Y-%m-%d')
                        horoscope_data = get_horoscope_by_day(zodiac_num, day)
                        return jsonify(success = True, data = horoscope_data, status=200)
                except KeyError:
                        raise NotFound('No such sign exists')
                except AttributeError:
                        raise BadRequest('Something went wrong; check the URL and the arguments')
                except ValueError:
                        raise BadRequest('Please enter date in correct format: YYYY-MM-DD')
@ns.route('/get-horoscope/weekly')
class WeeklyHoroscopeAPI(Resource):
    '''Shows weekly horoscope of zodiac signs'''
    @ns.doc(parser=parser)
    def get(self):
        args = parser.parse_args()
        zodiac_sign = args.get('sign')
        try:
            zodiac_num = ZODIAC_SIGNS[zodiac_sign.capitalize()]
            horoscope_data = get_horoscope_by_week(zodiac_num)
            return jsonify(success=True, data=horoscope_data, status=200)
        except KeyError:
            raise NotFound('No such zodiac sign exists')
        except AttributeError:
            raise BadRequest('Something went wrong, please check the URL and the arguments.')

@ns.route('/get-horoscope/monthly')
class MonthlyHoroscopeAPI(Resource):
    '''Shows monthly horoscope of zodiac signs'''
    @ns.doc(parser=parser)
    def get(self):
        args = parser.parse_args()
        zodiac_sign = args.get('sign')
        try:
            zodiac_num = ZODIAC_SIGNS[zodiac_sign.capitalize()]
            horoscope_data = get_horoscope_by_month(zodiac_num)
            return jsonify(success=True, data=horoscope_data, status=200)
        except KeyError:
            raise NotFound('No such zodiac sign exists')
        except AttributeError:
            raise BadRequest('Something went wrong, please check the URL and the arguments.')