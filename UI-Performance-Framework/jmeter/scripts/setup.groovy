import org.openqa.selenium.chrome.ChromeDriver
import org.openqa.selenium.chrome.ChromeOptions
import java.time.Duration
// Browser startup is outside the measured business sampler; each thread owns one driver.
int number = ctx.getThreadNum() + 1
if (number > 3) throw new IllegalArgumentException('Use at most three browser users for this local demo')
ChromeOptions options = new ChromeOptions()
if (props.getProperty('headless', 'true') == 'true') options.addArguments('--headless=new')
options.addArguments('--window-size=1366,900', '--disable-dev-shm-usage')
ChromeDriver driver = new ChromeDriver(options)
vars.putObject('driver', driver)
driver.manage().timeouts().implicitlyWait(Duration.ZERO)
driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(20))
vars.put('username', String.format('sample%02d', number))
vars.put('password', String.format('DemoOnly%02d!', number))
