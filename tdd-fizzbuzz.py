def test_fizzbuzz():
    assert 1 == fizzbuzz(1)
    assert 2 == fizzbuzz(2)
    assert 'Fizz' == fizzbuzz(3)
    assert 4 == fizzbuzz(4)
    assert 'Buzz' == fizzbuzz(5)
    assert 'Fizz' == fizzbuzz(6)
    assert 7 == fizzbuzz(7)
    assert 'FizzBuzz' == fizzbuzz(15)
    assert 'Fizz' == fizzbuzz(18)
    assert 'Buzz' == fizzbuzz(20)
    assert 'FizzBuzz' == fizzbuzz(30)


def fizzbuzz(num):
    if num % 3 == 0 and num % 5 == 0:
        return 'FizzBuzz'
    elif num % 3 == 0:
        return 'Fizz'
    elif num % 5 == 0:
        return 'Buzz'
    else:
        return num


test_fizzbuzz()
