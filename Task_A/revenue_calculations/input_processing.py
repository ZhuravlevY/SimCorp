import datetime as dt
from typing import Union, Dict

from revenue_calculations.errors import CalculationDateError, MinInvestmentValueError, InvestmentDurationError, \
    RateError, ExitError
from comons.global_variables import GlobalVariables as GV


def current_investment_term_in_months(agreement_date: dt.datetime, calculation_date: dt.datetime) -> int:
    _duration = (calculation_date.year - agreement_date.year) * GV.MONTH_IN_YEAR + \
                (calculation_date.month - agreement_date.month) - \
                (1 if calculation_date.day - agreement_date.day < 0 else 0)
    if _duration <= 0:
        raise CalculationDateError
    return _duration


def request_arg(message: str, data_type: str, agreement_date: dt.datetime = object) -> Union[int, float, dt.datetime]:
    while True:
        input_value = input(message)
        if input_value == 'q':
            raise ExitError
        try:
            if data_type == 'agreement':
                return dt.datetime.strptime(input_value, GV.DATE_FORMAT)
            elif data_type == 'calculation':
                calculation_date = dt.datetime.strptime(input_value, GV.DATE_FORMAT)
                current_investment_term_in_months(agreement_date, calculation_date)
                return calculation_date
            elif data_type == 'investment':
                investment = float(input_value)
                if investment < GV.MIN_INVESTMENT:
                    raise MinInvestmentValueError
                return investment
            elif data_type == 'rate':
                rate = float(input_value)
                if rate < 0 or rate > 100:
                    raise RateError
                return rate
            elif data_type == 'duration':
                duration = int(input_value)
                if duration < GV.MIN_INVESTMENT_DURATION:
                    raise InvestmentDurationError
                return duration
        except CalculationDateError:
            print(f"Calculation date ({input_value}) can't be before the agreement date "
                  f"({agreement_date.strftime(GV.DATE_FORMAT)})")
        except MinInvestmentValueError:
            print(f"Investment amount ({input_value}) must be greater than one cent")
        except RateError:
            print(f"Rate ({input_value}) must be greater than zero and less than a hundred")
        except InvestmentDurationError:
            print(f"Investment duration ({input_value}) must be an integer and greater than zero")
        except ValueError:
            print(f"Data {input_value} isn't matched the format")


def arg_request() -> Dict[str, Union[float, int, dt.datetime]]:
    required_args = {'agreement_date': dt.datetime,
                     'calculation_date': dt.datetime,
                     'investment': float,
                     'rate': float,
                     'investment_duration': int}
    for key in required_args.keys():
        if key == 'agreement_date':
            required_args[key] = \
                request_arg('Please enter a agreement date in the ddmmyyyy format (press q to exit): ', 'agreement')
        elif key == 'calculation_date':
            required_args[key] = \
                request_arg('Please enter a calculation date in the ddmmyyyy format (press q to exit): ', 'calculation',
                                             required_args['agreement_date'])
        elif key == 'investment':
            required_args[key] = \
                request_arg('Please enter a investment amount with no more than two decimal places (press q to exit): ',
                                             'investment')
        elif key == 'rate':
            required_args[key] = \
                request_arg('Please enter an interest rate from zero to a hundred (press q to exit): ', 'rate')
        elif key == 'investment_duration':
            required_args[key] = \
                request_arg('Please enter an investment duration in years (press q to exit): ', 'duration')
    return required_args
