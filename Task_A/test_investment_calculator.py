import unittest
import datetime as dt

from revenue_calculations.payments import body_first_payment, rate_payment
from revenue_calculations.input_processing import current_investment_term_in_months
from revenue_calculations.calculate_revenue import calc_payment_list, calc_interest_schedule, calc_months_left, \
    calc_sum_future_interest
from revenue_calculations.calculate_revenue import investment_calculator
from comons.global_variables import GlobalVariables as GV


class CalculatorTestCase(unittest.TestCase):
    test_list = [20.0, 19.755111046301966,
                 19.50777320306695,
                 19.257961981399582,
                 19.005652647515543,
                 18.750820220292663,
                 18.493439468797558,
                 18.233484909787496,
                 17.970930805187336,
                 17.705751159541173,
                 17.43791971743855,
                 17.1674099609149,
                 16.894195106826015,
                 16.61824810419624,
                 16.33954163154017,
                 16.058048094157535,
                 15.773739621401074,
                 15.48658806391705,
                 15.196564990858185,
                 14.903641687068733,
                 14.607789150241384,
                 14.308978088045762,
                 14.007178915228184,
                 13.702361750682433,
                 13.394496414491224,
                 13.0835524249381,
                 12.769498995489446,
                 12.452305031746306,
                 12.131939128365731,
                 11.808369565951354,
                 11.481564307912834,
                 11.151490997293926,
                 10.81811695356883,
                 10.481409169406485,
                 10.141334307402515,
                 9.797858696778503,
                 9.450948330048254,
                 9.1005688596507,
                 8.746685594549172,
                 8.389263496796628,
                 8.02826717806656,
                 7.6636608961491905,
                 7.295408551412647,
                 6.923473683228739,
                 6.547819466362991,
                 6.168408707328587,
                 5.785203840703836,
                 5.3981669254128395,
                 5.0072596409689325,
                 4.612443283680587,
                 4.213678762819358,
                 3.8109265967495163,
                 3.4041469090189764,
                 2.9932994244111306,
                 2.578343464957207,
                 2.159237945908744,
                 1.7359413716697958,
                 1.3084118316884585,
                 0.8766069963073079,
                 0.44048411257234577]

    def test_body_first_payment(self):
        body_first_payment_ = body_first_payment(2000, 0.01, 60)
        self.assertEqual(body_first_payment_, 24.488895369803522)

    def test_rate_payment(self):
        rate_payment_ = rate_payment(2000, 0.01)
        self.assertEqual(rate_payment_, 20)

    def test_duration_between_agreement_calculate_date(self):
        agreement_date = dt.datetime.strptime('01012000', GV.DATE_FORMAT)
        calculation_date = dt.datetime.strptime('01112000', GV.DATE_FORMAT)
        duration = current_investment_term_in_months(agreement_date, calculation_date)
        self.assertEqual(duration, 10)

    def test_calc_payment_list(self):
        list_all_rate_payment = calc_payment_list(2000, 44.488895369803522, 0.01, 60)
        self.assertEqual(list_all_rate_payment, self.test_list)

    def test_calc_interest_schedule(self):
        list_all_rate_payment = calc_interest_schedule(2000, 12, 5)
        self.assertEqual(list_all_rate_payment, self.test_list)

    def test_calc_months_left(self):
        agreement_date = dt.datetime.strptime('01012000', GV.DATE_FORMAT)
        calculation_date = dt.datetime.strptime('01112000', GV.DATE_FORMAT)
        list_all_rate_payment = calc_months_left(5, agreement_date, calculation_date)
        self.assertEqual(list_all_rate_payment, 50)

    def test_calc_sum_future_interest(self):
        sum_future_interest = calc_sum_future_interest([40, 30, 20, 10], 3)
        self.assertEqual(sum_future_interest, 60)

    def test_investment_calculator(self):
        agreement_date = dt.datetime.strptime('01012000', GV.DATE_FORMAT)
        calculation_date = dt.datetime.strptime('01112000', GV.DATE_FORMAT)
        input_data = {'agreement_date': agreement_date,
                      'calculation_date': calculation_date,
                      'investment': 2000,
                      'rate': 12,
                      'investment_duration': 5}
        sum_future_interest = investment_calculator(**input_data)
        self.assertEqual(sum_future_interest, 480.65)


unittest.main()
