from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from playwright.sync_api import sync_playwright
import logging
import tempfile
import os
import base64
from datetime import datetime
from io import BytesIO
from PIL import Image  # Add this for image validation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class InvoiceGenerator:
    def __init__(self):
        logger.info("Initializing Invoice Generator")
        self.template_dir = Path(__file__).parent / 'templates'
        logger.info(f"Template directory: {self.template_dir}")
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

    def calculate_totals(self, items):
        for item in items:
            item['amount'] = float(item['hours']) * item['rate']  # Ensure proper float handling
        return sum(item['amount'] for item in items)
    def get_image_base64(self, image_path):
        """Convert image to base64 with proper mime type and resize if needed"""
        try:
            logger.info(f"Attempting to open image: {image_path}")
            with Image.open(image_path) as img:
                logger.info(f"Successfully opened image with size: {img.size}")
                
                # Resize image to a more reasonable size for an invoice logo
                max_size = (300, 300)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                logger.info(f"Resized image to: {img.size}")
                
                # Save to bytes
                buffer = BytesIO()
                img.save(buffer, format="PNG", optimize=True)
                b64_data = base64.b64encode(buffer.getvalue()).decode()
                logger.info(f"Base64 encoded length: {len(b64_data)}")
                
                return f"data:image/png;base64,{b64_data}"
        except Exception as e:
            logger.error(f"Error in get_image_base64: {e}")
            logger.exception("Full traceback:")
            return None

    def generate(self, data, output_file=None):
        try:
            # Get absolute path for logo
            logo_path = Path(__file__).parent / 'static' / 'logo.jpg'
            logger.info(f"Looking for logo at: {logo_path.absolute()}")
            logger.info(f"Logo file exists: {logo_path.exists()}")

            # Generate filename if not provided
            if output_file is None:
                today = datetime.now().strftime('%Y-%m-%d')
                company_name = data['company']['name']
                output_file = f"[{today}] {company_name} Invoice.pdf"
            if logo_path.exists():
                logger.info("Logo file found, attempting to encode")
                data['logo_exists'] = True
                data['logo_url'] = self.get_image_base64(logo_path)
                
                if data['logo_url']:
                    logger.info("Logo successfully encoded")
                else:
                    logger.error("Logo encoding failed")
                    data['logo_exists'] = False
            else:
                logger.warning("Logo file not found")
                data['logo_exists'] = False

            # Calculate amounts
            total = self.calculate_totals(data['services'])
            data['total'] = total
            
            # Render HTML
            template = self.env.get_template('invoice.html')
            html_content = template.render(data=data)
            
            # Create temporary HTML file with explicit UTF-8 encoding
            with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <style>
                        {open(self.template_dir / 'style.css', 'r', encoding='utf-8').read()}
                    </style>
                </head>
                <body>
                    {html_content}
                </body>
                </html>
                """)
                temp_html = f.name

            # Generate PDF using playwright
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page(viewport={'width': 1200, 'height': 1600})  # Larger viewport
                page.goto(f'file://{temp_html}')
                page.wait_for_load_state('networkidle')
                page.pdf(
                    path=output_file,
                    format='A4',
                    print_background=True,
                    margin={
                        'top': '1cm',
                        'right': '1cm',
                        'bottom': '1cm',
                        'left': '1cm'
                    },
                    scale=0.95  # Slightly scale down to ensure proper fit
                )
                browser.close()

            # Cleanup temp file
            os.unlink(temp_html)
            
        except Exception as e:
            logger.error(f"Error generating invoice: {e}")
            logger.exception("Full traceback:")
            raise