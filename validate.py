def validate(fun, input_file, expected=None) -> bool:
    print('========================================')
    print(f'Testing: {fun.__name__}({input_file})')
    result = fun(input_file)
    if result != expected:
        if expected is not None:
            print('Expected:')
            print(expected)
        print('Got:')
        print(result)
        exit(1)
    else:
        print("OK!")
