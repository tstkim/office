# main.py
import config
import folder_setup
import product_name_extraction
import price_extraction
import thumbnail_extraction
import 스타스포츠.option_extraction_back as option_extraction_back
import detail_page_extraction

def main():
    print("Starting main script...")
    folder_setup.setup_folders()
    product_name_extraction.extract_product_names()
    price_extraction.extract_prices()
    thumbnail_extraction.extract_thumbnails()
    option_extraction_back.extract_options()
    detail_page_extraction.extract_detail_pages()
    print("Script completed successfully.")

if __name__ == "__main__":
    main()
