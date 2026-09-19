def driver = vars.getObject('driver')
try { if (driver != null) driver.quit() }
finally { vars.remove('driver') }
