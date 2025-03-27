from zapv2 import ZAPv2
import time

def run_zap_scan(target_url):
    zap = ZAPv2(apikey='your-api-key', proxies={'http': 'http://localhost:8080'})
    
    print('Starting scan...')
    scan_id = zap.ascan.scan(target_url)
    
    while int(zap.ascan.status(scan_id)) < 100:
        print(f'Scan progress: {zap.ascan.status(scan_id)}%')
        time.sleep(5)
    
    print('Scan completed!')
    return zap.ascan.alerts()
