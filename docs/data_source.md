
# Data Source Notes – Lab 1

## Data Type

This is **structured data** because it is organised in a clear tabular format with rows and columns. Each row represents one transaction and each column represents a specific attribute of that transaction.

## Variables (Columns)

| Column           | What it represents                                 |
| ---------------- | -------------------------------------------------- |
| Transaction ID   | Unique identifier for each transaction             |
| Item             | The product that was purchased (e.g. Coffee, Cake) |
| Quantity         | How many units of the item were bought             |
| Price Per Unit   | The price of one unit of the item                  |
| Total Spent      | The total amount paid for that transaction         |
| Payment Method   | How the customer paid (e.g. Cash, Credit Card)     |
| Location         | Where the purchase happened (In-store or Takeaway) |
| Transaction Date | The date the transaction took place                |

## Target and Features

- **Target variable:** `Total Spent`(This is the main value we would normally want to predict or analyse.)
- **Candidate features:**
  `Item`, `Quantity`, `Price Per Unit`, `Payment Method`, `Location`, `Transaction Date`

`Transaction ID` is just an identifier and would not normally be used as a feature.
