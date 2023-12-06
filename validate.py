def validate(fun, input_file, expected=None) -> bool:
    result = fun(input_file)
    if result != expected:
        print('========================================')
        if expected is not None:
            print('Expected:')
            print(expected)
        print('Got:')
        print(result)
        print(f'Tested: {fun.__name__}({input_file})')
        print('========================================')
        exit(1)
