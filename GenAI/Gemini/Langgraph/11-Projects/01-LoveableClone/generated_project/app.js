// app.js - Calculator core logic

/**
 * Calculator class handles input, display updates, and expression evaluation.
 */
class Calculator {
  /**
   * @param {HTMLElement} displayElement - The element where the current input/result is shown.
   */
  constructor(displayElement) {
    this.displayElement = displayElement;
    this.currentInput = '';
    this.updateDisplay();
  }

  /** Update the display element with the current input string. */
  updateDisplay() {
    // Support both input elements and other elements.
    if (this.displayElement instanceof HTMLInputElement) {
      this.displayElement.value = this.currentInput || '0';
    } else {
      this.displayElement.textContent = this.currentInput || '0';
    }
  }

  /** Append a character/value to the current input and refresh the display. */
  append(value) {
    this.currentInput += value;
    this.updateDisplay();
  }

  /** Clear the current input and reset the display. */
  clear() {
    this.currentInput = '';
    this.updateDisplay();
  }

  /** Remove the last character from the current input and refresh the display. */
  backspace() {
    this.currentInput = this.currentInput.slice(0, -1);
    this.updateDisplay();
  }

  /** Evaluate the current arithmetic expression safely.
   * Handles division by zero and malformed expressions.
   */
  calculate() {
    if (!this.currentInput) {
      return;
    }
    // Allow only numbers, parentheses and basic operators.
    const safeExpression = this.currentInput.replace(/[^0-9+\-*/().]/g, '');
    try {
      // Using Function constructor for simple arithmetic evaluation.
      // "use strict" prevents access to the surrounding scope.
      const result = Function('"use strict";return (' + safeExpression + ')')();
      if (!isFinite(result)) {
        throw new Error('Division by zero');
      }
      this.currentInput = String(result);
      this.updateDisplay();
    } catch (e) {
      // Show a generic error and reset input.
      if (this.displayElement instanceof HTMLInputElement) {
        this.displayElement.value = 'Error';
      } else {
        this.displayElement.textContent = 'Error';
      }
      this.currentInput = '';
    }
  }

  /** Handle keyboard events and map them to calculator actions. */
  handleKey(event) {
    const key = event.key;
    if (/^[0-9]$/.test(key) || key === '.' || ['+', '-', '*', '/'].includes(key)) {
      this.append(key);
    } else if (key === 'Enter' || key === '=') {
      this.calculate();
    } else if (key === 'Backspace') {
      this.backspace();
    } else if (key === 'Escape') {
      this.clear();
    }
    // Prevent default for handled keys.
    const handledKeys = ['Enter', 'Backspace', 'Escape', '=', '+', '-', '*', '/', '.'];
    for (let i = 0; i <= 9; i++) handledKeys.push(String(i));
    if (handledKeys.includes(key)) {
      event.preventDefault();
    }
  }
}

// Export the class for module environments (e.g., testing) and expose globally.
if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
  module.exports = Calculator;
} else {
  window.Calculator = Calculator;
}

// Instantiate the calculator with the display element from the DOM.
const displayEl = document.getElementById('display');
if (!displayEl) {
  throw new Error('Display element with id "display" not found in the DOM.');
}
const calc = new Calculator(displayEl);

// Attach click listeners to all buttons with the class .btn.
const buttons = document.querySelectorAll('.btn');
buttons.forEach((btn) => {
  const action = btn.dataset.action;
  const value = btn.dataset.value; // For digit, operator, decimal etc.
  btn.addEventListener('click', () => {
    switch (action) {
      case 'clear':
        calc.clear();
        break;
      case 'backspace':
        calc.backspace();
        break;
      case 'equals':
        calc.calculate();
        break;
      case 'add':
      case 'subtract':
      case 'multiply':
      case 'divide':
        // Legacy actions – map to operator symbols.
        const opMap = { add: '+', subtract: '-', multiply: '*', divide: '/' };
        calc.append(opMap[action]);
        break;
      case 'digit':
      case 'decimal':
      case 'operator':
        // Use the explicit data-value if present, otherwise fallback to innerText.
        calc.append(value || btn.innerText.trim());
        break;
      default:
        // Fallback: treat button text as value.
        const txt = btn.innerText.trim();
        if (txt) calc.append(txt);
        break;
    }
  });
});

// Keyboard support.
document.addEventListener('keydown', (e) => calc.handleKey(e));
