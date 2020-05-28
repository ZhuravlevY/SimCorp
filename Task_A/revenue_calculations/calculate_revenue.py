from typing import List, Dict, Union
import datetime as dt

from revenue_calculations.payments import body_first_payment, rate_payment
from revenue_calculations.input_processing import current_investment_term_in_months
from revenue_calculations.input_processing import arg_request
from revenue_calculations.errors import ExitError
from comons.global_variables import GlobalVariables as GV


def calc_payment_list(investment: float,
                      month_payment: float,
                      month_rate: float,
                      month_investment_duration: int) -> List[float]:
    _body_balance = investment
    _duration = month_investment_duration
    list_all_rate_payment = []

    while _duration > 0:
        _rate_payment = rate_payment(_body_balance, month_rate)
        list_all_rate_payment.append(_rate_payment)
        _body_payment = month_payment - _rate_payment
        _body_balance -= _body_payment
        _duration -= 1
    return list_all_rate_payment


def calc_interest_schedule(investment: float, rate: float, investment_duration: int) -> List[float]:
    month_rate = rate / GV.MONTH_IN_YEAR / 100
    month_investment_duration = investment_duration * GV.MONTH_IN_YEAR

    _body_first_payment = body_first_payment(investment, month_rate, month_investment_duration)
    rate_first_payment_ = rate_payment(investment, month_rate)
    month_payment = _body_first_payment + rate_first_payment_
    list_all_rate_payment = calc_payment_list(investment, month_payment, month_rate, month_investment_duration)
    return list_all_rate_payment


def calc_months_left(investment_duration: int, agreement_date: dt.datetime, calculation_date: dt.datetime) -> int:
    return investment_duration * GV.MONTH_IN_YEAR - current_investment_term_in_months(agreement_date, calculation_date)


def calc_sum_future_interest(list_all_rate_payment: List[float], months_left: int) -> float:
    return sum(list_all_rate_payment[-months_left:])


def investment_calculator(**kwargs):
    try:
        # if no arguments provided then request them from console
        if not kwargs:
            input_data: Dict[str, Union[float, int, dt.datetime]] = arg_request()
        else:
            input_data = kwargs
        list_all_rate_payment = calc_interest_schedule(input_data['investment'], input_data['rate'],
                                                       input_data['investment_duration'], )
        months_left = calc_months_left(input_data['investment_duration'], input_data['agreement_date'],
                                       input_data['calculation_date'])
        sum_future_interest = calc_sum_future_interest(list_all_rate_payment, months_left)
        rounded_sum_future_interest = round(sum_future_interest, GV.ROUNDING_MARK)

        # if no arguments provided then print result to the console
        if not kwargs:
            print(rounded_sum_future_interest)
        return rounded_sum_future_interest
    except ExitError:
        None
