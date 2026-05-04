# SimpleCalculatorWebApp

## Project Overview

SimpleCalculatorWebApp is a lightweight, responsive web‑based calculator built with vanilla **HTML**, **CSS**, and **JavaScript**. It provides a clean user interface that works on both desktop and mobile browsers, allowing users to perform basic arithmetic operations quickly and reliably.

## Features

- **Responsive UI** – The layout adapts to different screen sizes, ensuring a pleasant experience on phones, tablets, and desktops.
- **Arithmetic Operations** – Supports addition, subtraction, multiplication, division, and decimal calculations.
- **Clear & Backspace** – Dedicated buttons to clear the entire expression or delete the last character.
- **Keyboard Support** – Users can type numbers and operators directly from the keyboard; `Enter`/`=` evaluates, `Esc` clears, and `Backspace` deletes.
- **Error Handling** – Detects division by zero and malformed expressions, displaying an `Error` message without crashing the app.

## Tech Stack

- **HTML** – Structure of the calculator and button elements.
- **CSS** – Styling and responsive layout.
- **JavaScript** – Core calculator logic (`app.js`), event handling, and expression evaluation.

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository‑url>
   cd <repository‑directory>
   ```
2. **Open the application**
   - Locate the `index.html` file in the project root.
   - Open it in any modern web browser (Chrome, Firefox, Edge, Safari, etc.).
   - No build tools, package managers, or server setup are required.

## Usage Guide

### UI Layout

- **Display** – Shows the current input or result. It defaults to `0` when empty.
- **Buttons** – Arranged in a grid:
  - Digits `0‑9`
  - Decimal point `.`
  - Operators `+`, `-`, `*`, `/`
  - `C` (Clear) – resets the entire expression.
  - `←` (Backspace) – removes the last character.
  - `=` (Equals) – evaluates the expression.

### Button Functions

- **Digits / Decimal** – Append the corresponding character to the current expression.
- **Operators** – Append `+`, `-`, `*`, or `/`.
- **Clear (`C`)** – Clears the whole input and resets the display to `0`.
- **Backspace (`←`)** – Deletes the last character entered.
- **Equals (`=`)** – Evaluates the expression and shows the result. If an error occurs (e.g., division by zero), `Error` is displayed.

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `0‑9` | Append digit |
| `.` | Append decimal point |
| `+`, `-`, `*`, `/` | Append operator |
| `Enter` or `=` | Evaluate expression |
| `Backspace` | Delete last character |
| `Escape` | Clear the entire input |

All supported keys prevent the default browser behavior to keep the calculator focused.

### Error Display

When the calculator encounters an invalid expression or attempts division by zero, the display changes to **`Error`**. The internal input buffer is cleared, allowing the user to start a new calculation immediately.

## Contributing

Contributions are welcome! If you find a bug or have an idea for improvement:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Ensure the UI remains responsive and the existing tests (if any) pass.
4. Submit a pull request with a clear description of the changes.

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.
