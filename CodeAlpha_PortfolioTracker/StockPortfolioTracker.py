"""Task 2: Stock Portfolio Tracker"""

import csv
from datetime import date
from pathlib import Path

STOCK_PRICES: dict[str, float] = {
    "AAPL": 180.00,
    "TSLA": 250.00,
    "MSFT": 420.00,
    "NVDA": 120.00,
    "GOOGL": 175.00,
    "AMZN": 190.00,
}
CSV_FILENAME = "observatory_portfolio.csv"
LINE = "-" * 72


def read_input(prompt: str) -> str | None:
    """Read input, returning None if the input stream is closed."""
    try:
        return input(prompt).strip()
    except EOFError:
        return None


def display_welcome() -> None:
    print("\n" + "=" * 72)
    print("                    PORTFOLIO OBSERVATORY")
    print("                 A simple stock portfolio tracker")
    print("=" * 72)
    print("Demo prices are fixed sample values in USD; they are not live quotes.")
    print("Supported symbols: " + ", ".join(sorted(STOCK_PRICES)))


def display_menu() -> None:
    print("\n" + LINE)
    print("MAIN MENU")
    print("  1  Add shares to a holding")
    print("  2  View portfolio dashboard")
    print("  3  Remove shares from a holding")
    print("  4  Export portfolio to CSV")
    print("  5  Show sample prices")
    print("  0  Exit")
    print(LINE)


def display_stock_prices() -> None:
    print("\nSAMPLE PRICE LIST - USD PER SHARE")
    print(LINE)
    print(f"{'SYMBOL':<12}{'PRICE':>16}")
    print(LINE)

    for ticker, price in sorted(STOCK_PRICES.items()):
        print(f"{ticker:<12}${price:>14,.2f}")

    print(LINE)


def get_positive_integer(prompt: str) -> int | None:
    """Ask until a positive whole number is entered or the user cancels."""
    while True:
        value = read_input(prompt + " (or press Enter to cancel): ")

        if value is None or value == "":
            print("No changes made.")
            return None

        try:
            quantity = int(value)
        except ValueError:
            print("Please enter a whole number, such as 3.")
            continue

        if quantity <= 0:
            print("The number of shares must be greater than zero.")
            continue

        return quantity


def add_holding(holdings: dict[str, int]) -> None:
    value = read_input("Enter a stock symbol (or press Enter to cancel): ")

    if value is None or value == "":
        print("Add operation cancelled.")
        return

    ticker = value.upper()

    if ticker not in STOCK_PRICES:
        print(
            f"'{ticker}' is not supported. "
            f"Choose from: {', '.join(sorted(STOCK_PRICES))}."
        )
        return

    quantity = get_positive_integer(
        f"How many {ticker} shares would you like to add?"
    )

    if quantity is None:
        return

    holdings[ticker] = holdings.get(ticker, 0) + quantity
    value = holdings[ticker] * STOCK_PRICES[ticker]

    print(
        f"Added {quantity} {ticker} share(s). "
        f"New holding: {holdings[ticker]} share(s), worth about ${value:,.2f}."
    )


def remove_holding(holdings: dict[str, int]) -> None:
    if not holdings:
        print("Your portfolio is empty. Add a holding before removing shares.")
        return

    value = read_input(
        "Enter the symbol to reduce or remove (or press Enter to cancel): "
    )

    if value is None or value == "":
        print("Remove operation cancelled.")
        return

    ticker = value.upper()

    if ticker not in holdings:
        print(f"{ticker} is not currently in your portfolio.")
        return

    current_quantity = holdings[ticker]
    current_value = current_quantity * STOCK_PRICES[ticker]
    print(
        f"Current holding: {current_quantity} {ticker} share(s), "
        f"worth about ${current_value:,.2f}."
    )

    while True:
        answer = read_input(
            "Remove the entire holding? [y/n] "
            "(or press Enter to cancel): "
        )

        if answer is None or answer == "":
            print("No changes made.")
            return

        answer = answer.lower()

        if answer in {"y", "yes"}:
            del holdings[ticker]
            print(f"Removed all {ticker} shares from the portfolio.")
            return

        if answer in {"n", "no"}:
            quantity = get_positive_integer(
                f"How many {ticker} shares would you like to remove?"
            )

            if quantity is None:
                return

            if quantity > current_quantity:
                print(
                    f"You only own {current_quantity} {ticker} share(s). "
                    "No changes made."
                )
                return

            remaining = current_quantity - quantity

            if remaining == 0:
                del holdings[ticker]
                print(f"Removed the final {ticker} share. Holding closed.")
            else:
                holdings[ticker] = remaining
                remaining_value = remaining * STOCK_PRICES[ticker]
                print(
                    f"Removed {quantity} share(s). Remaining: "
                    f"{remaining} {ticker} share(s), "
                    f"worth about ${remaining_value:,.2f}."
                )
            return

        print("Please enter y or n.")


def display_dashboard(holdings: dict[str, int]) -> None:
    print("\nPORTFOLIO DASHBOARD")
    print(f"As of {date.today().isoformat()} - Sample prices in USD")
    print(LINE)

    if not holdings:
        print("Your portfolio is empty. Choose 'Add shares' to get started.")
        print(LINE)
        return

    print(f"{'SYMBOL':<10}{'SHARES':>10}{'PRICE / SHARE':>20}{'EST. VALUE':>20}")
    print(LINE)

    total_value = 0.0

    for ticker in sorted(holdings):
        quantity = holdings[ticker]
        price = STOCK_PRICES[ticker]
        value = quantity * price
        total_value += value

        print(
            f"{ticker:<10}{quantity:>10,}"
            f"{('$' + format(price, ',.2f')):>20}"
            f"{('$' + format(value, ',.2f')):>20}"
        )

    print(LINE)
    print(f"{'TOTAL ESTIMATED VALUE':<40}${total_value:>18,.2f}")
    print("Estimates use fixed sample prices, not live market quotes.")
    print(LINE)


def export_to_csv(holdings: dict[str, int]) -> None:
    output_path = Path(CSV_FILENAME)

    try:
        with output_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                [
                    "symbol",
                    "shares",
                    "sample_price_usd",
                    "estimated_value_usd",
                    "as_of",
                ]
            )

            for ticker in sorted(holdings):
                quantity = holdings[ticker]
                price = STOCK_PRICES[ticker]
                value = quantity * price

                writer.writerow(
                    [
                        ticker,
                        quantity,
                        f"{price:.2f}",
                        f"{value:.2f}",
                        date.today().isoformat(),
                    ]
                )

        print(f"Portfolio exported to: {output_path.resolve()}")

        if not holdings:
            print("The portfolio is empty, so the CSV contains only column headers.")

    except OSError as error:
        print(f"Could not write the CSV file: {error}")


def main() -> None:
    holdings: dict[str, int] = {}

    display_welcome()

    while True:
        display_menu()
        choice = read_input("Select an option [0-5]: ")

        if choice is None:
            print("\nInput closed. Goodbye.")
            return

        if choice == "1":
            add_holding(holdings)
        elif choice == "2":
            display_dashboard(holdings)
        elif choice == "3":
            remove_holding(holdings)
        elif choice == "4":
            export_to_csv(holdings)
        elif choice == "5":
            display_stock_prices()
        elif choice == "0":
            print("\nThanks for using Portfolio Observatory. Goodbye!")
            return
        else:
            print("Invalid choice. Enter a number from 0 to 5.")


if __name__ == "__main__":
    main()
