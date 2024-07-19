import re
import os
import csv
import datetime
import requests
import uuid
import glob

from RPA.Excel.Files import Files

# Method to create the "images" folder where it will store the images
def create_image_folder() -> None:
    dir = "./output/images"
    if not os.path.exists(dir):
        os.makedirs(dir)

# Method to create the "result" folder where it will store the result
def create_csv_folder() -> None:
    dir = "./output/result"
    if not os.path.exists(dir):
        os.makedirs(dir)

# Method to select the wished range date
def set_month_range(number_of_months: int) -> tuple[str, str]:
    today = datetime.date.today()
    end = today.strftime("%m/%d/%Y")
    if number_of_months < 2:
        start = today.replace(day=1).strftime("%m/%d/%Y")
    else:
        start = (
            (today - datetime.timedelta(days=30 * (number_of_months - 1)))
            .replace(day=1)
            .strftime("%m/%d/%Y")
        )
    return start, end

# Method to convert the datetime
def replace_date_with_hour(date: str) -> str: 
    
    actual_date =  datetime.datetime.now()  
     
    months = {
        'Jan.': '01', 'Feb.': '02', 'Mar.': '03', 'Apr.': '04',
        'May.': '05', 'Jun.': '06', 'Jul.': '07', 'Aug.': '08',
        'Sep.': '09', 'Oct.': '10', 'Nov.': '11', 'Dec.': '12'
    }
    
    # Checking if the date format value is like '8h ago'
    if re.match(r'^(\d+)h ago$', date):
        hours = int(re.match(r'^(\d+)h ago$', date).group(1))
        date_now = actual_date - datetime.timedelta(hours=hours)
        date = date_now.strftime('%m/%d/%Y')
        return date
    # Checking if the date format value is like 'Jun. 8, 2017'
    elif re.match(r'[A-Z][a-z]{2}\. \d{1,2}, \d{4}', date):
        parts = date.split()
        month = months[parts[0]]  # Convert month to a numeric value
        day = parts[1].strip(',')  # remove the comma
        year = parts[2]
        date = f"{month}/{day}/{year}"
        return date
    # Checking if the date format value is like 'June 27'
    elif re.match(r'([A-Z][a-z]+) \d{1,2}', date):
        date += f" {str(actual_date.year)}"
        date_obj = datetime.datetime.strptime(date, '%B %d %Y')
        date = date_obj.strftime('%m/%d/%Y')
        return date
    return date

# Method to write the result data in excel file
def write_excel_data(data: list) -> None:   
    header = [
        'Title',
        'Date',
        'Description',
        'Image_Name',
        'Title_Contains "$"',
        'Description_Contains "$"',
        'Phrases_Count_in_Title'
    ]
    # Inserting the header in the excel file
    data.insert(0, header)
    # Creating the excel file
    lib = Files()
    lib.create_workbook()
    # Writing the data result in excel file
    lib.append_rows_to_worksheet(data)
    # Saving the excel file with name "result.xlsx"
    lib.save_workbook(f"./output/result/result.xlsx")

# Method to save and rename the image files
def download_image_from_url(image_url: str) -> str:
    image_name = str(uuid.uuid4())
    if image_url == "":
        return ""
    img_data = requests.get(image_url).content
    with open(f"./output/images/{image_name}.jpg", "wb") as handler:
        handler.write(img_data)
    return image_name

# Method to count how many times wished phrases is contained in the title element
def check_phrases(text_pattern: str, text: str, count=0) -> int:
    c = count
    words = text.split()
    for word in words:
        if word.strip(",.;:-?!").upper() == text_pattern.upper():
            c += 1
    return c

# Method to check dolar symbol in title and description element
def check_for_dolar_sign(text: str) -> bool:
    pattern = re.compile(
        "((\$\s*\d{1,}.\d{0,}.\d{0,})|(\d{1,}\s*(dollars|usd|dollar)))", re.IGNORECASE
    )

    if re.search(pattern, text):
        return True
    return False

# Method to get all images files from folder
def get_all_files_from_folder(path="./output/images/*.jpg"):
    files = glob.glob(path)
    return files


