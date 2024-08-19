// Dependencies
const assert = require("assert")

// Configuration
const URL = "https://abtester.app"
const TITLE = "streamlitApp"  // HTML title attribute of the desired iframe.
const TEXT = "18,508 is the minimum sample size required."

// Set timeouts for page load and element finding.
await $webDriver.manage().setTimeouts({
  pageLoad: 30000,  // 30 seconds for page load timeout.
  implicit: 5000,  // 5 seconds for element finding timeout.
});

console.log("Starting the synthetic script.")

console.log("Navigating to:", URL)
await $webDriver.get(URL)

console.log("Finding the iframe with the title:", TITLE)
var By = $selenium.By
var iframe = await $webDriver.findElement(
  By.xpath("//iframe[@title='" + TITLE + "']")
)

console.log("Switching to the iframe.")
await $webDriver.switchTo().frame(iframe)

console.log("Clicking the button to calculate.")
await $webDriver.findElement(By.xpath("//button[@kind='primary']")).click()

console.log("Checking for the presence of an element with the text:", TEXT)
var element = await $webDriver.findElement(
  By.xpath("//*[text()='" + TEXT + "']")
)
var textFound = await element.getText()
console.log("Found text:", textFound)
assert.equal(textFound, TEXT, "Expected text not found on the page.")

console.log("Script completed successfully.")
