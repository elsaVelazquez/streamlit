-- Use the FROSTY_SAMPLE database
USE FROSTY_SAMPLE;

-- Create the CHATBOT schema if it doesn't exist (unnecessary if it already exists)
CREATE SCHEMA IF NOT EXISTS FROSTY_SAMPLE.CHATBOT;

-- Create a table equivalent to the FINANCIAL_ENTITY_ATTRIBUTES_LIMITED view
CREATE TABLE IF NOT EXISTS CHATBOT.FINANCIAL_ENTITY_ATTRIBUTES_LIMITED (
    variable VARCHAR(255),
    definition TEXT
    -- Include other columns that are selected in the view creation script above
);

-- Create a table equivalent to the FINANCIAL_ENTITY_ANNUAL_TIME_SERIES view
CREATE TABLE IF NOT EXISTS CHATBOT.FINANCIAL_ENTITY_ANNUAL_TIME_SERIES (
    entity_name VARCHAR(255),
    city VARCHAR(255),
    state_abbreviation VARCHAR(255),
    variable_name VARCHAR(255),
    year INT,
    value DOUBLE,
    unit VARCHAR(255),
    definition TEXT
    -- Include other columns that are selected in the view creation script above
);


CREATE TABLE IF NOT EXISTS CHATBOT.RESTAURANT_TIME_SERIES (
    date DATE,
    restaurant_name VARCHAR(255),
    review TEXT,
    rating INTEGER
);

INSERT INTO CHATBOT.RESTAURANT_TIME_SERIES (date, restaurant_name, review, rating)
VALUES
('2022-01-01', 'Mexican Restaurant', 'Great food!', 5),
-- Add more rows as needed
('2022-01-02', 'Soup-On', 'Average experience.', 3);

-- Confirm the table was created correctly and view sample data