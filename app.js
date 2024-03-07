const buttons = document.querySelectorAll("button");
const currCalc = document.querySelector("#calculation");
const currInput = document.querySelector("#input");

const checkRE = /(\d|\))$/; // RegExp matches, if last character of string is number or ')'
const re1 = /(0+)$/g; // RegExp matches all 0 at the en of a string
const re2 = /\.$/; // RegExp matches dot at the end
let calc = [];
let input = [];
let res;
let intRes = false;
let disCalc = [];
let disResult;
let str;

function onNumber(el) {
  // print number, unless user tries to input multiple zeros in the beginning & input-display is full
  if (
    ((el === "0" && (input[0] !== "0" || input.includes("."))) || el !== "0") &&
    input.length < 20
  ) {
    input[0] === "0" && !input.includes(".") && el !== "0"
      ? (input = [])
      : input;
    input.push(el);
    currInput.innerHTML = `${input.join("")}`;
  }
}

function onClear(el) {
  if (el === "c") {
    // clear all
    calc = [];
    input = [];
    intRes = false;
    res = undefined;
    displayCalculation(calc, false);
    currInput.innerHTML = "";
    // console.log(calc, input, negative, intRes, res);
  } else if (el === "ce") {
    // clear entry (input)
    input = [];
    currInput.innerHTML = "";
  } else if (el === "del" && input.length > 0) {
    // delete last input character
    input.splice(-1);
    currInput.innerHTML = `${input.join("")}`;
  }
}

function onNeg() {
  // toggle between ± only if input is not 0
  if (input.length !== 0 && eval(input.join("")) !== 0) {
    let negative;
    input[0] === "-" ? (negative = true) : (negative = false);
    // if-condition for display-reasons
    if ((!negative && input.length < 20) || negative) {
      negative ? input.shift() : input.unshift("-");
      currInput.innerHTML = `${input.join("")}`;
    }
  }
}

function onDot() {
  // print dot, unless input is already a decimal & condition for display-reasons
  if (!input.includes(".") && input.length < 20) {
    input.length > 0 ? input.push(".") : input.push("0", ".");
    currInput.innerHTML = `${input.join("")}`;
  }
}

function onOperator(operator) {
  // eliminate redundant 0 from input end(re1), and dot if necessary(re2)
  input.join("").includes(".") && re1.test(input.join(""))
    ? (input = input
        .join("")
        .replace(re1, "")
        .replace(re2, "")
        .split(""))
    : input;
  // run only, if input ends with checkRE OR
  // calc isn't empty and ends with checkRE =>  || (calc.length > 0 && checkRE.test(calc))
  if (checkRE.test(input)) {
    // input in calc, dependend if input is negative or not ; then reset input
    eval(input.join("")) < 0
      ? calc.push(`(${input.join("")})`)
      : calc.push(`${input.join("")}`);
    input = [];
    // operator in calc
    calc.push(operator);
    // display current input and calc
    displayCalculation(calc, false);
    currInput.innerHTML = `${input.join("")}`;
  }
}

function onEqual() {
  // eliminate redundant 0 from input end(re1), and dot if necessary(re2)
  input.join("").includes(".") && re1.test(input.join(""))
    ? input = input
        .join("")
        .replace(re1, "")
        .replace(re2, "")
        .split("")
    : input;
  // run only if input ends with checkRE
  if (checkRE.test(input)) {
    // input in calc, dependend if input is negative or not ; then reset input
    eval(input.join("")) < 0
      ? calc.push(`(${input.join("")})`)
      : calc.push(`${input.join("")}`);
    input = [];
    // resolve calculation, only if calc ends with checkRE
    if (checkRE.test(calc)) {
      res = eval(calc.join(""));
      // display calculation and result
      displayCalculation(calc, true);
      displayResult(res);
    }
  }
}

function followUp(withIntRes) {
  if (withIntRes) {
    input = res.toString().split("");
  }
  calc = [];
  res = undefined;
  intRes = undefined;
  currCalc.innerHTML = `${calc}`;
}

function displayResult(res) {
  if (res > 99999999999999999999 || res < -9999999999999999999) {
    disResult = "error";
    calc = [];
    input = [];
    res = [];
    intRes = false;
    displayCalculation([], false);
  } else {
    disResult = res;
    intRes = true;
  }
  currInput.innerHTML = `${disResult}`;
}

function displayCalculation(calcArr, final) {
  final ? calcArr.push("=") : calcArr;
  str = calcArr.join("");
  if (str.length > 30) {
    str = str.substr(-29);
    disCalc = `…${str}`;
  } else {
    disCalc = str;
  }
  currCalc.innerHTML = disCalc;
}

function calculator() {
  if (this.className === "number") {
    if (intRes) {
      followUp(false);
    }
    onNumber(this.id);
  } else if (this.className === "clear") {
    onClear(this.id);
  } else if (this.id === "negative") {
    if (intRes) {
      followUp(true);
    }
    onNeg();
  } else if (this.className === "dot") {
    if (intRes) {
      followUp(false);
    }
    onDot();
  } else if (this.className === "operator") {
    if (intRes) {
      followUp(true);
    }
    onOperator(this.id);
  } else if (this.className === "equal") {
    onEqual();
  }
}

buttons.forEach(button => button.addEventListener("click", calculator));
