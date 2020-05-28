def body_first_payment(investment: float, rate: float, investment_duration: int) -> float:
    return (investment * rate) / (((1 + rate) ** investment_duration) - 1)


def rate_payment(body_balance: float, rate: float) -> float:
    return body_balance * rate
