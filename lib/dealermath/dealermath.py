class DealerMath():

    @staticmethod
    def mojo_to_xch_str(mojos=int):
        max_send_amount_xch = (mojos / 1000000000000)
        return(f'{max_send_amount_xch:.12f}')

    @staticmethod
    def calculate_proportion(total_amount=int, percentage=float):
        if DealerMath.is_between(0.0, percentage, 100.0):
            return(int((percentage / 100) * total_amount))
        else:
            raise Exception(f"Percentage values must be between 0.0 and 100.0! Specified: {str(percentage)}")

    @staticmethod
    def check_sum(sum_elements=list, expected_total_value=float):
        if all(isinstance(x, float) for x in sum_elements):
            if sum(sum_elements) != expected_total_value:
                raise Exception(f"The sum of {str(' + '.join(map(str, sum_elements)))} is not equal to {str(expected_total_value)}!")
        else:
            raise Exception(f"NOT all percentage values are written as floats!")

    @staticmethod
    def is_between(a, x, b):
        return min(a, b) <= x <= max(a, b)