# Invoice Generator

A Python-based invoice generator that creates professional PDF invoices from structured data. The system supports custom company branding, client information, and detailed service itemization.

## Features

- Generate professional PDF invoices
- Custom company branding with logo support
- Automated business day calculations for due dates
- Detailed service itemization with rate calculations
- Responsive template design
- Configurable company and client information
- Clean, modern invoice layout
- Automatic total calculations

## Prerequisites

- Python 3.8 or higher
- Playwright browser automation framework
- Pillow for image processing
- Jinja2 templating engine

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd invoice-generator
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install
```

4. Set up your configuration:
```bash
cp config_example.py config.py
```

## Configuration

Edit `config.py` with your specific details:

```python
CONFIG = {
    'invoice_number': '1',
    'company': {
        'name': 'Your Company Name',
        'street': 'Company Street Address',
        'city': 'Company City',
        'state': 'Company State',
        'zip': 'Company ZIP'
    },
    'client': {
        'name': 'Client Company Name',
        'contact': 'Client Contact Name',
        'phone': 'Client Phone Number',
        'email': 'client@email.com'
    },
    'service_rates': {
        'Software Engineering Consultation': 75.00
    },
    'services': [
        {
            'type': 'Service Type',
            'date': 'MM/DD/YYYY',
            'description': 'Service Description',
            'hours': 0
        }
    ]
}
```

## Custom Branding

To add your company logo:
1. Place your logo image in `src/static/logo.jpg`
2. The image will be automatically resized to fit the invoice header
3. Supported format: JPG

## Usage

Run the invoice generator:

```bash
python src/main.py
```

The generator will:
1. Load your configuration
2. Calculate business days for the due date
3. Apply service rates
4. Generate a PDF invoice in the current directory

## Directory Structure

```
├── config_example.py       # Template configuration file
├── requirements.txt        # Python dependencies
├── src/
│   ├── invoice.py         # Invoice generation logic
│   ├── main.py           # Main application entry point
│   ├── static/           # Static assets
│   │   └── logo.jpg      # Company logo
│   └── templates/        # Invoice templates
│       ├── invoice.html  # Invoice HTML template
│       └── style.css     # Invoice styling
```

## Customization

- Edit `src/templates/invoice.html` to modify the invoice layout
- Update `src/templates/style.css` to change the invoice styling
- Modify `src/invoice.py` to add new features or change the generation logic

## Features in Detail

### Business Day Calculation
- Automatically calculates due dates excluding weekends
- Default payment term: 10 business days

### PDF Generation
- Uses Playwright for reliable PDF generation
- Supports custom page sizes and margins
- Maintains consistent styling across different systems

### Template System
- Jinja2 templating for flexible invoice layouts
- Responsive design that adapts to content
- Support for custom styling and branding

## Security Considerations

- Sensitive information is stored in `config.py` (gitignored)
- Use environment variables for production deployments
- Regularly update dependencies for security patches