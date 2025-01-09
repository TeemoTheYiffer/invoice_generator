from invoice import InvoiceGenerator
from datetime import datetime, timedelta
import logging
from config import CONFIG

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def add_business_days(start_date, business_days):
    """Add business days to a date, skipping weekends"""
    current_date = start_date
    remaining_days = business_days
    
    while remaining_days > 0:
        current_date += timedelta(days=1)
        # Check if it's a weekend (5 = Saturday, 6 = Sunday)
        if current_date.weekday() < 5:
            remaining_days -= 1
            
    return current_date

def create_invoice_data(services):
    """Create invoice data using configuration and service details"""
    issue_date = datetime.now()
    
    return {
        'invoice_number': CONFIG['invoice_number'],
        'issue_date': issue_date,
        'due_date': add_business_days(issue_date, 10),
        'company': CONFIG['company'],
        'client': CONFIG['client'],
        'services': services
    }

def main():
    logger.info("Starting invoice generation process")

    # Add rates to services from config
    services = [
        {**service, 'rate': CONFIG['service_rates'][service['type']]}
        for service in CONFIG['services']
    ]

    # Generate invoice data
    invoice_data = create_invoice_data(services)

    # Generate invoice
    generator = InvoiceGenerator()
    generator.generate(invoice_data)

if __name__ == '__main__':
    main()
