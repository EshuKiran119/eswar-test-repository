import org.openqa.selenium.By
import org.openqa.selenium.support.ui.WebDriverWait
import org.openqa.selenium.support.ui.ExpectedConditions
import java.time.Duration

def driver = vars.getObject('driver')
if (driver == null) return
try {
    def buttons = driver.findElements(By.id('logout'))
    if (!buttons.empty && buttons[0].displayed) {
        buttons[0].click() // Demo app deletes its owned order and invalidates the session.
        new WebDriverWait(driver, Duration.ofSeconds(10)).until(
            ExpectedConditions.visibilityOfElementLocated(By.id('username')))
    }
} finally {
    // Failed teardown remains a failed JTL row and fails the gate.
    driver.executeScript('sessionStorage.clear()')
}
