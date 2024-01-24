CREATE SCHEMA IF NOT EXISTS FROSTY_SAMPLE.CHATBOT;

CREATE OR REPLACE TABLE FROSTY_SAMPLE.CHATBOT.Synthetic_Sales_Data AS (
    SELECT *
    FROM (
        VALUES
            ('Company A', 'New York', 'NY', 'Net Sales', 2020, 'USD', 'Net sales represent the revenue from sales after deductions...', 200.00),
            ('Company B', 'Los Angeles', 'CA', 'Gross Sales', 2020, 'USD', 'Gross sales represent the revenue from all sales...', 400.00),
            ('Company A', 'New York', 'NY', 'Net Sales', 2021, 'USD', 'Net sales represent the revenue from sales after deductions...', 500.00),
            ('Company B', 'Los Angeles', 'CA', 'Gross Sales', 2021, 'USD', 'Gross sales represent the revenue from all sales...', 600.00),
            ('Company A', 'New York', 'NY', 'Net Sales', 2022, 'USD', 'Net sales represent the revenue from sales after deductions...', 700.00)
    ) AS t("ENTITY_NAME", "CITY", "STATE_ABBREVIATION", "VARIABLE_NAME", "YEAR", "UNIT", "DEFINITION", "VALUE")
);




CREATE OR REPLACE TABLE Synthetic_Retail_Data AS  
    SELECT 
        "Retailer ID", 
        "Retailer Name", 
        "Retailer SKU", 
        "UPC", 
        "Model Number", 
        "Title", 
        "Brand", 
        "Category", 
        "Subcategory", 
        "Week ID", 
        "Month", 
        "Year", 
        "Traffic Type" AS "VARIABLE_NAME", -- Ensure this matches the exact casing as the column was created
        "Traffic Description" AS "DEFINITION", 
        "Traffic Value" AS "Value"
    FROM (  
        SELECT * FROM VALUES  
            (1, 'Megastore.com', 'A1ALS6K1KP', '', '', 'Waterless Dog Shampoo, Volumizing Dog Shampoo for All Hair Types', 'SHIFAKOU', 'Hair Care', 'Dog Shampoo', 202319, 5, 2023, 'Organic Traffic', 'Organic traffic represents the visitors...', 100),  
            (2, 'Megastore.com', 'A1ALS6K1KP', '', '', 'Waterless Dog Shampoo, Volumizing Dog Shampoo for All Hair Types', 'SHIFAKOU', 'Hair Care', 'Dog Shampoo', 202320, 5, 2023, 'Paid Traffic', 'Paid traffic represents the visitors...', 200)
            -- Add more rows as needed for your synthetic data
    ) AS t(
        "Retailer ID", 
        "Retailer Name", 
        "Retailer SKU", 
        "UPC", 
        "Model Number", 
        "Title", 
        "Brand", 
        "Category", 
        "Subcategory", 
        "Week ID", 
        "Month", 
        "Year", 
        "Traffic Type", 
        "Traffic Description", 
        "Traffic Value"
    );
