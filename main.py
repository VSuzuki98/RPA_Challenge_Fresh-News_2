# docs for RPA lib > https://rpaframework.org/libdoc/RPA_Browser_Selenium.html
import logging
logging.basicConfig(level='INFO')
from RPA.Browser.Selenium import Selenium
from RPA.Robocorp.WorkItems import WorkItems

# Importing the methods though 'setup.py' file
from setup import URL, SEARCH_PHRASE, NUMBER_OF_MONTHS, CATEGORY
# Importing the methods though 'util.py' file
from util import (
    set_month_range,
    write_excel_data,
    replace_date_with_hour,
    download_image_from_url,
    check_for_dolar_sign,
    check_phrases,
    create_image_folder,
    create_csv_folder,
    get_all_files_from_folder,
)

# Defining class 'WebScraper'
class WebScraper:
    def __init__(self):
        # Creating object 'browser_lib' from class 'Selenium'
        self.browser_lib = Selenium()

    # Method to close the browser
    def close_browser(self) -> None:
        self.browser_lib.close_browser()

    # Method to open the browser and access the website
    def open_website(self, url: str) -> None:
        self.browser_lib.open_chrome_browser(url,maximized=True)

    # Method to close popup browser
    def popup_exists(self) -> None:
        popup_accept = "//button[@data-testid='Accept all-btn']"
        self.browser_lib.wait_until_element_is_visible(locator=popup_accept, timeout="60")
        popup_bottom_accept = self.browser_lib.does_page_contain_button(popup_accept)
        if popup_bottom_accept:
            self.browser_lib.click_button(locator=popup_accept)

    # Method to search the wished phrase in website
    def begin_search(self, search_phrase: str) -> None:
        try:
            search_xpath = "//*[@id='app']//button[@data-testid='search-button']"
            self.browser_lib.click_button(locator=search_xpath)
            field_xpath = "//input[@placeholder='SEARCH']"
            self.browser_lib.input_text(locator=field_xpath, text=search_phrase)
            go_button_xpath = "//button[@type='submit']"
            self.browser_lib.click_button_when_visible(locator=go_button_xpath)

        except ValueError as e:
            raise f"Error on execution of begin_search -> {e}"

    # Method to select the wished category in website
    def select_category(self, categorys) -> None:
        if len(categorys) == 0:
            return
        for value in categorys:
            try:
                section_drop_btn = "//div[@data-testid='section']/button[@data-testid='search-multiselect-button']"
                self.browser_lib.click_button_when_visible(locator=section_drop_btn)
                sections_list = "//*[@data-testid='section']//li"
                self.browser_lib.wait_until_page_contains_element(locator=sections_list)
                section = f"//input[@data-testid='DropdownLabelCheckbox' and contains(@value, '{value}')]"
                self.browser_lib.click_element(section)

            except:
                print(f"Category not found")

    # Method to select the newest news in website
    def sort_newest_news(self, list_value="newest") -> None:
        try:
            sort_dropdow_button = "//select[@data-testid='SearchForm-sortBy']"
            self.browser_lib.select_from_list_by_value(sort_dropdow_button, list_value)

        except ValueError as e:
            raise f"Error on execution of sort_newest_news -> {e}"

    # Method to select the wished date range in website
    def set_date_range(self, number_of_months: int) -> None:
        try:
            date_button = "//button[@data-testid='search-date-dropdown-a']"
            self.browser_lib.click_button_when_visible(locator=date_button)
            specific_dates_button = "//button[@value='Specific Dates']"
            self.browser_lib.click_button_when_visible(locator=specific_dates_button)
            input_date_range_start = "//input[@id='startDate']"
            input_date_range_end = "//input[@id='endDate']"
            date_start, date_end = set_month_range(number_of_months)
            self.browser_lib.input_text(input_date_range_start, date_start)
            self.browser_lib.input_text(input_date_range_end, date_end)
            self.browser_lib.click_button_when_visible(locator=date_button)

        except ValueError as e:
            raise f"Error on execution of data range -> {e}"

    # Method to get 'path' value from element value
    def get_element_value(self, path: str) -> str:
        if self.browser_lib.does_page_contain_element(path):
            return self.browser_lib.get_text(path)
        return ""

    # Method to get image value
    def get_image_value(self, path: str) -> str:
        if self.browser_lib.does_page_contain_element(path):
            return self.browser_lib.get_element_attribute(path, "src")
        return ""

    #Method to click in "Show more" option in website to see more news
    def load_all_news(self) -> None:
        show_more_button = "//button[@data-testid='search-show-more-button']"
        while self.browser_lib.does_page_contain_button(show_more_button):
            try:
                self.browser_lib.wait_until_page_contains_element(locator=show_more_button, timeout='15')
                self.browser_lib.scroll_element_into_view(locator=show_more_button)
                self.browser_lib.click_element(show_more_button)
            except:
                print("Page show more button done")

    # Method to extract website data
    def extract_website_data(self, search_phrase: str) -> None:
        try:
            # Creating a list to store the data results
            extracted_data = []
            # Loading all news from website through 'Show more' option
            self.load_all_news()
            # Getting the web elements from website list results
            element_list = "//ol[@data-testid='search-results']/li[@data-testid='search-bodega-result']"
            news_list_elements = self.browser_lib.get_webelements(element_list)
            # Iteracting in each web element returned and taking the specific data
            for value in range(1, len(news_list_elements) + 1):                
                # Taking the title value element
                title_element = self.get_element_value(f"{element_list}[{value}]//h4")
                
                # Taking and editing the date value element
                date_element = replace_date_with_hour(self.get_element_value(f"{element_list}[{value}]//span[@data-testid]"))
                
                # Taking the description value element
                description_element = self.get_element_value(f"{element_list}[{value}]//a/p")
                
                # Taking the image value element and downloading the picture in a folder
                image_element = download_image_from_url(self.get_image_value(f"{element_list}[{value}]//img"))
                
                # Taking the values counted though search phrase value in the title element
                phrases_count = check_phrases(text_pattern=search_phrase, text=title_element)

                # Checking if the title contains dolar symbol with method below
                title_contains_dolar = check_for_dolar_sign(title_element)
                
                # Checking if the description contains dolar symbol with method below
                description_contains_dolar = check_for_dolar_sign(description_element)

                # Filling the data results in the list below
                extracted_data.append(
                    [
                        title_element,
                        date_element,
                        description_element,
                        image_element,
                        title_contains_dolar,
                        description_contains_dolar,
                        phrases_count
                    ]
                )
            # Filling the data results in csv file in a folder
            write_excel_data(extracted_data)
        # Handle specific exception to execute the method      
        except ValueError as e:
            raise f"Error on execution of select_category -> {e}"

    # Main function
    def main(self) -> None:
        try:
            # Step 1 - Creating a folder to put images with method below
            create_image_folder()
                
            # Step 2 - Creating a folder to put csv file result with method below
            create_csv_folder()
            
            # Step 3 - Instancing the object 'workIt' from class 'WorkItems'
            workIt = WorkItems()
            
            # Step 4 - Getting the data from file 'data' from folder './devdata/work-items-in'          
            workIt.get_input_work_item()
            
            # Step 5 - Getting the values variables from file 'data' from folder './devdata\work-items-in'
            url = workIt.get_work_item_variable("url")
            search_phrase = workIt.get_work_item_variable("search_phrase")
            category = workIt.get_work_item_variable("category")
            number_of_months = workIt.get_work_item_variable("number_of_months")
            
            # Step 6 - Opening the website with Google browser
            self.open_website(url=url)
            
            # Step 7 - Threading to close popup browser
            self.popup_exists()
            
            # Step 8 - Searching the wished phrase in website
            self.begin_search(search_phrase=search_phrase)
            
            # Step 9 - Selecting the wished category in website
            self.select_category(categorys=category)
            
            # Step 10 - Selecting the option 'newest' in website
            self.sort_newest_news()
            
            # Step 11 - Selecting the wished range date in website
            self.set_date_range(number_of_months=number_of_months)
            
            # Step 12 - Extracting the website data in website and saving in csv file
            self.extract_website_data(search_phrase=search_phrase)
            
            # Step 13 - Adding the csv file in the folder for work-items-out
            workIt.add_work_item_file("./output/result/result.xlsx", "RESULT_EXCEL.xlsx")
            
            # Step 14 - Getting all the picture files in the folder
            files = get_all_files_from_folder()
            
            # Step 15 - Creating the result image and files folder for work-items-out
            workIt.create_output_work_item(files=files, save=True)
            workIt.create_output_work_item(files="./output/result/result.xlsx", save=True)

        finally:
            # Step 16 - Closing the website and browser
            self.close_browser()


if __name__ == "__main__":
    # Step - Instancing the object 'scraper' from class 'WebScraper'
    scraper = WebScraper()
    scraper.main()
