def bank_withdrawal(balance: float, withdrawal_amount: float) -> float:
    """
    Simulates a bank withdrawal with exception handling.

    Args:
        balance: Current account balance
        withdrawal_amount: Amount to withdraw

    Returns:
        Updated balance after successful withdrawal
    """
    print(f"\n{'=' * 45}")
    print(f"  💳 BANK WITHDRAWAL SYSTEM")
    print(f"{'=' * 45}")
    print(f"  Current Balance  : ${balance:,.2f}")
    print(f"  Withdrawal Amount: ${withdrawal_amount:,.2f}")
    print(f"{'=' * 45}")

    try:
        # Validate input
        if withdrawal_amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")

        # Check if withdrawal exceeds balance
        if withdrawal_amount > balance:
            raise OverflowError(
                f"Insufficient funds! "
                f"Requested: ${withdrawal_amount:,.2f}, "
                f"Available: ${balance:,.2f}"
            )

        # Perform withdrawal
        new_balance = balance - withdrawal_amount

    except ValueError as ve:
        print(f"\n  ❌ INVALID INPUT: {ve}")
        new_balance = balance  # Balance unchanged
        status = "FAILED (Invalid Input)"

    except OverflowError as oe:
        print(f"\n  ❌ TRANSACTION DENIED: {oe}")
        new_balance = balance  # Balance unchanged
        status = "FAILED (Insufficient Funds)"

    else:
        # Runs only if no exception was raised
        print(f"\n  ✅ TRANSACTION SUCCESSFUL!")
        print(f"  Amount Debited   : ${withdrawal_amount:,.2f}")
        print(f"  Remaining Balance: ${new_balance:,.2f}")
        status = "SUCCESS"

    finally:
        # Always runs — log the transaction
        print(f"\n  📋 TRANSACTION LOG")
        print(f"  {'─' * 35}")
        print(f"  Opening Balance  : ${balance:,.2f}")
        print(f"  Attempted Debit  : ${withdrawal_amount:,.2f}")
        print(f"  Closing Balance  : ${new_balance:,.2f}")
        print(f"  Status           : {status}")
        print(f"{'=' * 45}\n")

    return new_balance


# ── Demo Scenarios ──────────────────────────────────────

if __name__ == "__main__":
    account_balance = 1500.00

    # Scenario 1: Successful withdrawal
    account_balance = bank_withdrawal(account_balance, 200.00)

    # Scenario 2: Withdrawal exceeds balance
    account_balance = bank_withdrawal(account_balance, 5000.00)

    # Scenario 3: Invalid (negative) amount
    account_balance = bank_withdrawal(account_balance, -50.00)

    # Scenario 4: Exact balance withdrawal
    account_balance = bank_withdrawal(account_balance, account_balance)