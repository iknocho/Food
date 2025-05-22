from look_and_say import center_two_digits

def main():
    """사용자로부터 입력을 받아 Look and Say 수열의 중간 두 자리를 출력합니다."""
    try:
        n = int(input("양의 정수 n을 입력하세요 (4 <= n <= 99): "))
        result = center_two_digits(n)
        print(f"Look and Say 수열의 {n}번째 항의 가운데 두 자릿수는: {result}")
    except ValueError as e:
        print(f"오류: {e}")

if __name__ == "__main__":
    main()