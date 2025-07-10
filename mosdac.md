# MOSDAC - Meteorological and Oceanographic Satellite Data Archival Centre

## Overview
MOSDAC is a Data Centre of Space Applications Centre (SAC) operated by Indian Space Research Organisation (ISRO), Government of India. It provides satellite data reception, processing, analysis and dissemination services.

Website: https://www.mosdac.gov.in/
Organization: Space Applications Centre, Indian Space Research Organisation (ISRO)

## How to Download INSAT-3DR Dataset

### Step-by-Step Download Process
1. Visit https://www.mosdac.gov.in/ and click "Sign Up" to register as a new user
2. Fill the registration form with your personal and professional details
3. Submit the registration form and check your email for verification link
4. Click the verification link in a new browser window to activate your account
5. Return to https://www.mosdac.gov.in/ and login with your credentials
6. Click "Satellite data order" from the main menu
7. Navigate to the data catalog and search for INSAT-3DR datasets
8. Select the specific INSAT-3DR products you need (Imager, Sounder, or both)
9. Add selected datasets to your cart
10. Submit your data request and note down the request ID provided
11. Wait for email notification confirming your data is ready for download
12. Use SFTP client to connect to sftp://ftp.mosdac.gov.in with your MOSDAC credentials
13. Download the processed INSAT-3DR data files

### Important Download Notes
INSAT-3DR data requires user registration and has a 3-day latency restriction for L1 data. Your SFTP credentials are the same as your MOSDAC portal login credentials. INSAT-3DR products are identical to INSAT-3D products.

## How to Register for MOSDAC Account

### Registration Steps
1. Go to https://www.mosdac.gov.in/
2. Click "Sign Up" button to access registration form
3. Fill in required personal details including name, email, organization
4. Provide professional information and intended use of data
5. Submit the completed registration form
6. Check your email inbox for verification message
7. Copy the verification link from email and paste in new browser window
8. Your account will be activated and ready for data ordering

### Account Management
After registration, you can reset your password using the "Forgot Password" link. If you enter wrong credentials 3 times, your account will be locked for 1 hour. Always use the same credentials for both portal access and SFTP downloads.

## How to Access INSAT-3DR Data Catalog

### Catalog Navigation Steps
1. Visit https://www.mosdac.gov.in/
2. Click "Catalog" in the top navigation menu
3. Select "Satellite data" from the dropdown menu
4. Look for INSAT-3DR in the active missions section
5. Review available products with their specifications, start dates, end dates, and frequency
6. Click on specific products to view detailed information including abstract and technical specifications

### INSAT-3DR Product Information
INSAT-3DR is a dedicated meteorological spacecraft weighing approximately 2211 kg. It is configured on I-2K bus with Sounder, Imager, Data Relay Transponder (DRT), and Satellite Aided Search & Rescue (SAS&R) payloads. The satellite provides enhanced meteorological observations and monitoring for land and ocean surface monitoring, weather forecasting, and disaster warning.

## How to Check Data Request Status

### Status Tracking Process
1. Login to your MOSDAC account at https://www.mosdac.gov.in/
2. Navigate to "My request" tab in your user dashboard
3. View all submitted requests with their current processing status
4. Check request ID and processing stage for each order
5. Download links will appear when your requested data is ready
6. You will also receive email notifications when data processing is complete

## How to Use SFTP for Data Download

### SFTP Connection Setup
1. Download and install an SFTP client such as WinSCP, FileZilla, or use command line
2. Configure connection with Host: ftp.mosdac.gov.in, Protocol: SFTP, Port: 22
3. Enter your MOSDAC portal username and password as SFTP credentials
4. Connect to the server and navigate to your designated data folder
5. Download your requested INSAT-3DR files to your local computer

### SFTP Command Line Example
For command line users, connect using: sftp username@ftp.mosdac.gov.in
Navigate to your data folder using: cd /path/to/your/data
Download files using: get filename.ext or get -r directory_name

## How to Access Real-Time INSAT-3DR Data

### MOSDAC-LIVE Access
1. Visit https://mosdac.gov.in/live/index_one.php for real-time data access
2. Select INSAT-3DR from the available satellite options
3. Choose between Imager and Sounder data products
4. Select your preferred time range and geographical region of interest
5. View real-time data visualization and analysis tools
6. Download current data products directly from the live interface

MOSDAC-LIVE is a web-enabled data and information visualization system that provides access to satellite data products and information derived from satellites and model forecasts on a near real-time basis.

## INSAT-3DR Technical Specifications

### Satellite Configuration
INSAT-3DR is a dedicated meteorological spacecraft with a lift mass of approximately 2211 kg. It is configured on the I-2K bus platform and carries multiple payloads for comprehensive meteorological monitoring.

### Payloads and Capabilities
1. Meteorological Payloads: IMAGER and SOUNDER for atmospheric measurements
2. Data Relay Transponder (DRT) for communication relay services
3. Satellite Aided Search and Rescue (SAS&R) for emergency response
4. IMAGER provides imaging capability from geostationary altitude in visible (0.52-0.72 μm) and infrared channels
5. SOUNDER provides atmospheric profile measurements for weather forecasting

### Data Products Available
INSAT-3DR provides products identical to INSAT-3D including meteorological imagery, atmospheric soundings, and derived products for weather forecasting and disaster warning applications.

## Alternative Data Access Methods

### Open Data Access
Some INSAT-3DR datasets may be available through the "Open Data" section without requiring registration. Check the Open Data section on the main website for directly accessible datasets with limited time periods and specific products.

### Bulk Data Services
For large volume historical data downloads, use the SFTP services which are optimized for bulk data transfer. This method is most suitable for researchers and institutions requiring extensive data archives.

## Troubleshooting Common Issues

### Email Verification Problems
If you don't receive the verification email, check your spam folder first. If the verification link doesn't work when clicked, copy the entire verification link and paste it into a new browser window or tab instead of clicking directly.

### Password Reset Issues
When using the password reset function, if the reset link doesn't work when clicked, copy the reset link from your email and paste it into a new browser window or tab. This resolves most password reset problems.

### Account Lockout Resolution
If your account gets locked after 3 unsuccessful login attempts, you must wait exactly 1 hour before attempting to login again. The system will automatically unlock your account after this waiting period.

### SFTP Connection Problems
If you cannot connect to the SFTP server, verify that your credentials exactly match your MOSDAC portal login details. Check your firewall settings and ensure your SFTP client is configured with the correct server details: ftp.mosdac.gov.in, port 22.

### Data Download Delays
L1 data has a mandatory 3-day latency restriction for registered users. If your data is not immediately available, check back after this latency period. Higher level processed products may be available sooner.

## Data Processing and Quality Information

### Data Levels and Processing
INSAT-3DR data is available in multiple processing levels including L1B radiometrically calibrated data, L2 derived atmospheric and surface parameters, and L3 gridded and composite products. All data undergoes radiometric calibration based on ground calibration data using both ground and on-board calibration techniques.

### Data Formats and Compatibility
INSAT-3DR data is provided in standard meteorological data formats compatible with common analysis software. The data includes comprehensive metadata and quality flags to ensure proper interpretation and usage.

## INSAT-3DR vs Other Satellites

### When to Choose INSAT-3DR
Select INSAT-3DR for advanced meteorological applications, real-time weather monitoring, current weather conditions, forecasting applications, and disaster management scenarios requiring optimal disaster warning and emergency response capabilities.

### Alternative Satellite Options
INSAT-3D provides the same products as INSAT-3DR as the predecessor satellite. INSAT-3DS is part of the INSAT series with similar capabilities. For ocean-specific monitoring applications, consider OCEANSAT-3 which is optimized for ocean monitoring with specialized payloads.

## User Support and Documentation

### Getting Technical Support
For technical issues, contact MOSDAC support through the website contact options. For data-related questions, refer to the comprehensive product documentation available in the satellite data catalog. For account problems, use the password reset function or contact support directly.

### Available Documentation
Product specifications are available in the satellite data catalog section. User guides can be found in the documentation section for detailed operational guidance. A dedicated SFTP guide is available as a PDF download for detailed SFTP usage instructions.

## Additional Services and Features

### API Access and Integration
MOSDAC provides programmatic access to data catalogs through API services. This enables integration with automated analysis workflows and real-time data streaming capabilities for advanced users and research institutions.

### Customized Data Products
Users can request region-specific data extraction, custom time series generation, and specialized processing for research applications. These services are particularly useful for focused research projects requiring specific data formats or processing.

## Website Navigation Quick Reference

### Main Navigation Paths
- Main Portal: https://www.mosdac.gov.in/
- User Registration: Main page → Sign Up
- Data Ordering: Login → Satellite data order  
- Request Status: Login → My request tab
- Data Catalog: Catalog → Satellite data → INSAT-3DR
- Real-time Data: https://mosdac.gov.in/live/index_one.php
- SFTP Server: sftp://ftp.mosdac.gov.in

### Key User Actions
Registration is required for all data access. Login using verified credentials for data ordering. Select products and submit requests through the ordering system. Download processed data using SFTP with your portal credentials. Monitor request status through the user dashboard.

## Data Availability and Restrictions

### Access Requirements
User registration is mandatory for all INSAT-3DR data ordering and download. Some limited open data may be available without registration, but full access to the complete INSAT-3DR archive requires a verified user account.

### Data Latency Information
L1 data has a 3-day latency restriction for registered users. Higher level processed products may be available with shorter latency periods. Real-time data is available through MOSDAC-LIVE for immediate access needs.

### Download Limitations
While there are no specific download volume limits mentioned, large volume downloads should use SFTP services which are designed for bulk data transfer. Users should plan downloads appropriately based on their data volume requirements.