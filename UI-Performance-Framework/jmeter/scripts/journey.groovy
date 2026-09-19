import org.openqa.selenium.By
import org.openqa.selenium.support.ui.WebDriverWait
import org.openqa.selenium.support.ui.ExpectedConditions
import org.openqa.selenium.support.ui.Select
import java.time.Duration

def driver = vars.getObject('driver')
if (driver == null) throw new IllegalStateException('Browser initialization failed')
def wait = new WebDriverWait(driver, Duration.ofSeconds(10))
String origin = props.getProperty('base_url', 'http://127.0.0.1:8765')
// Time covers navigation, login, order submission and visible confirmation.
// It excludes driver startup, cleanup and pacing, and is not a Core Web Vitals measure.
driver.get(origin + '/login')
wait.until(ExpectedConditions.visibilityOfElementLocated(By.id('username'))).sendKeys(vars.get('username'))
driver.findElement(By.id('password')).sendKeys(vars.get('password'))
driver.findElement(By.cssSelector('#login-form button')).click()
wait.until(ExpectedConditions.visibilityOfElementLocated(By.id('product')))
new Select(driver.findElement(By.id('product'))).selectByValue('notebook')
def quantity = driver.findElement(By.id('quantity'))
quantity.clear(); quantity.sendKeys('2')
driver.findElement(By.cssSelector('#order-form button')).click()
def confirmation = wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector('[data-testid="order-total"]')))
assert confirmation.text == '$25.00'
assert !driver.findElement(By.cssSelector('[data-testid="order-id"]')).text.empty
SampleResult.setResponseCode('200')
SampleResult.setResponseMessage('Synthetic checkout completed with the expected visible total')
