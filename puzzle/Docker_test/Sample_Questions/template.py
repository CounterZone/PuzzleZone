# solution code
class your_solution_class:
    def your_method_name(your_args):
        pass

# test code
from solution import your_solution_class  # the class defined in the solution code

class test: # don't change this line
    def run_test(self,test_args):# don't change this line
        '''
        test_args: string. the test_args in the testcases(the assigned result not included).
        '''
        your_args=your_parser(test_args) # you need to parse your test args
        result=your_solution_class.your_method_name(your_args)
        return your_seralizer(result) # you need to return a string that could be compared with the test_result


SETTING={
# FAIL_MESSAGE would show for every case not passed
'FAIL_MESSAGE':'test case {test_case_id}:failed!\nfailed case: {test_args}\nexpected result:{test_result}\nyour result:{user_result}\n',
# PASS_MESSAGE would show for every case passed
'PASS_MESSAGE':'test case {test_case_id}:passed!\n',
#
'SAMPLE_TEST_SIZE':10
}

# testcases
# every line:
(test_args):(test_result)
