'''
the file running inside the docker container
receive the test_args from the command line
commands:
--test_args [test_args]
        test with test_args, print the result(only the last line would be the result)
--get_settings
        print settings defined in test_code
        settings:
            SAMPLE_SIZE
            FAIL_MESSAGE
            PASS_MESSAGE
'''
import argparse,json
from test import test,SETTING
cmd_parser=argparse.ArgumentParser()
cmd_parser.add_argument('--test_args')
cmd_parser.add_argument('--get_settings',action='store_true')
args=cmd_parser.parse_args()
if args.get_settings:
    print(json.dumps(SETTING))
else:
    test_args=args.test_args
    test_instance=test()
    result=test_instance.run_test(test_args)
    print('#RESULT')
    print(result,end='')
