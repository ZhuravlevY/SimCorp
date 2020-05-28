Please install Python 3.7.6.

The main run file is run_investment_calculator.py.

You can run it in the console and then input required params. 
Also, you can call the investment_calculator function with the required params. 

The simple example below:         
input_data = {'agreement_date': agreement_date,
                      'calculation_date': calculation_date,
                      'investment': 2000,
                      'rate': 12,
                      'investment_duration': 5}
        sum_future_interest = investment_calculator(**input_data)

The test cases can be run using test_investment_calculator.py.