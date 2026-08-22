-- Create the PostgreSQL database used by PricePulse
CREATE DATABASE pricepulse;

-- Create a dedicated PostgreSQL user for the PricePulse application
CREATE USER pricepulse WITH PASSWORD 'pricepulse';

-- Give the PricePulse user access to the PricePulse database
GRANT ALL PRIVILEGES ON DATABASE pricepulse TO pricepulse;