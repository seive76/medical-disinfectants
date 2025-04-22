# medical-disinfectants

A comprehensive data analysis project to gather, process, and visualize data related to medical disinfectants, including stakeholders such as competitors, clients, regulations, and overseas manufacturers.

## Project Overview

This project aims to provide detailed insights into the medical disinfectants market by analyzing various data sources including public databases, sales data, and web-scraped information.

## Data Sources

### Public Data Center
Primary data source: [data.go.kr](https://www.data.go.kr/index.do)

Key datasets include:
1. Disinfectants registered with detailed information
2. Sales volumes of imported and manufactured disinfectants
3. Hospital locations
4. Hospital detailed information (equipment installations)

### Additional Data Sources
- Web-scraped sales data
- Historical sales records (2017-2021)
- News articles
- Social media data (Twitter)
- Regulatory information from Google Sheets

## Project Components

### 1. Data Collection and Processing
- API integration with Korean medical data services
- Web scraping for sales and market data
- Historical data processing
- News and social media data collection
- Twitter API integration for market sentiment analysis

### 2. Main Analysis Components

#### Disinfectant Analysis
- Detailed product information tracking
- Active ingredients analysis
- Product attributes including:
  - Product codes
  - Manufacturer information
  - Approval dates
  - Storage methods
  - Validity periods
  - Safety information
  - Ingredients
  - ATC codes

#### Sales Analysis
- Historical sales data (2017-2021)
- Imported vs. manufactured product analysis
- Market trend analysis
- Sales data integration and processing

### 3. Technical Stack
- Python-based analysis
- Key libraries:
  - pandas for data manipulation
  - requests for API calls
  - BeautifulSoup for web scraping
  - tweepy for Twitter API integration
  - gspread for Google Sheets integration
- CSV-based data storage
- Jupyter notebooks for interactive analysis

## Project Structure

# Public data usage guideline
IROS_398_의약품_제품_허가정보_v1.4
https://docs.google.com/document/d/1H2eLOlKPOUM_oBIWKTP5qO81QzrJZr4H/edit?usp=sharing&ouid=114096873499970035150&rtpof=true&sd=true

## Public Data Usage Guidelines

For detailed information about the medical product authorization data format, refer to:
IROS_398_의약품_제품_허가정보_v1.4
[Documentation Link](https://docs.google.com/document/d/1H2eLOlKPOUM_oBIWKTP5qO81QzrJZr4H/edit?usp=sharing&ouid=114096873499970035150&rtpof=true&sd=true)

## Setup and Dependencies

Required Python packages:
```bash
numpy>=1.22.3
pandas
requests
beautifulsoup4
tweepy
gspread
oauth2client
schedule
```

Install dependencies using:
```bash
pip install -r requirements.txt
```

## API Configuration

The project requires several API keys for different services:
1. Korean Public Data Portal API key
2. Twitter API credentials
3. Google Sheets API credentials

Please ensure you have the necessary API keys configured in the appropriate configuration files.

## License

See the [LICENSE](LICENSE) file for details.

