# main.py
import config
import folder_setup
import product_name_extraction
import price_extraction
import thumbnail_extraction
import option_extraction
import detail_page_extraction

def main():
    print("Starting main script...")
    folder_setup.setup_folders()
    product_name_extraction.extract_product_names()
    price_extraction.extract_prices()
    thumbnail_extraction.extract_thumbnails()
    option_extraction.extract_options()
    detail_page_extraction.extract_detail_pages()
    print("Script completed successfully.")

if __name__ == "__main__":
    main()
