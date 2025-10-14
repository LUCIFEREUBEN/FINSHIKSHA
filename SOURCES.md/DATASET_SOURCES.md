# FinLit AI - Dataset Sources and References

## Official Government Sources

### 1. Securities and Exchange Board of India (SEBI)
**Organization:** Government of India - Securities Regulator
**Content Used:** Financial Education Booklet covering:
- Basics of saving and investment
- Understanding mutual funds
- Stock market basics
- Investor rights and grievances
- Financial frauds awareness

**Official Links:**
- Main Portal: https://investor.sebi.gov.in/
- Education Booklet: https://investor.sebi.gov.in/pdf/downloadable-documents/Financial%20Education%20Booklet%20-%20English.pdf
- Investor Awareness: https://investor.sebi.gov.in/educational-material.html

**Citation:** SEBI Investor Education and Protection Fund Authority, "Financial Education Booklet", 2024

---

### 2. Reserve Bank of India (RBI)
**Organization:** Central Bank of India
**Content Used:** Financial education materials on:
- Banking products (savings, current accounts)
- Loans and EMI calculations
- Digital payments (UPI, NEFT, RTGS)
- Credit management
- Financial frauds prevention

**Official Links:**
- Financial Education: https://www.rbi.org.in/financialeducation/
- FAME Portal: https://www.rbi.org.in/financialeducation/fame.aspx
- Publications: https://www.rbi.org.in/Scripts/PublicationsView.aspx

**Citation:** Reserve Bank of India, "Financial Awareness Messages (FAME)", 2024

---

### 3. National Centre for Financial Education (NCFE)
**Organization:** Joint initiative of financial sector regulators (RBI, SEBI, IRDAI, PFRDA)
**Content Used:** National Financial Literacy Survey data
- Financial literacy levels across Indian states
- Savings and investment patterns
- Digital payment adoption
- Insurance penetration

**Official Links:**
- Main Portal: https://ncfe.org.in/
- Survey Report: https://ncfe.org.in/wp-content/uploads/2023/12/NCFE-2019_Final_Report.pdf
- NSFE Strategy: https://ncfe.org.in/nsfe/

**Citation:** National Centre for Financial Education, "Financial Literacy and Inclusion in India Survey Report", 2019

---

## Public Datasets

### 4. Indian Personal Finance and Spending Habits Dataset
**Source:** Kaggle (Community Data Science Platform)
**Size:** 20,000+ records
**Content:**
- Monthly income distribution
- Expenditure patterns across categories
- Savings behavior
- EMI and loan data
- Demographics (age, occupation, location)

**Access:** https://www.kaggle.com/datasets/shriyashjagtap/indian-personal-finance-and-spending-habits

**Citation:** Jagtap, S. (2024). "Indian Personal Finance and Spending Habits Dataset". Kaggle.

**Usage in Project:** Used to understand real financial behavior patterns and create realistic examples

---

### 5. Financial Q&A Dataset - 10K
**Source:** Kaggle
**Size:** 10,000 question-answer pairs
**Content:**
- General financial literacy questions
- Investment concepts
- Banking terminology
- Financial planning advice

**Access:** https://www.kaggle.com/datasets/yousefsaeedian/financial-q-and-a-10k

**Citation:** Saeedian, Y. (2024). "Financial Q&A - 10K Dataset". Kaggle.

**Usage in Project:** Used as reference for question formulation patterns and answer structures

---

### 6. ADB Financial Literacy Survey
**Source:** Asian Development Bank Data Library
**Content:**
- Financial literacy survey results for Asian countries
- India-specific financial behavior data
- Comparative analysis across demographics

**Access:** https://data.adb.org/dataset/selected-financial-literacy-survey-results

**Citation:** Asian Development Bank (2023). "Selected Financial Literacy Survey Results". ADB Data Library.

**Usage in Project:** Used for benchmarking and understanding regional financial literacy levels

---

## Additional References

### 7. Ministry of Statistics and Programme Implementation (MoSPI)
**Household Finance Data:**
- Savings patterns
- Debt distribution
- Asset ownership

**Link:** https://mospi.gov.in/136-saving-and-capital-formation

---

### 8. Pradhan Mantri Jan Dhan Yojana (PMJDY) Data
**Source:** Government of India
**Data on:**
- Bank account penetration
- Digital payment adoption
- Financial inclusion metrics

**Link:** https://www.data.gov.in/catalog/pradhan-mantri-jan-dhan-yojana-pmjdy

---

## Data Processing Methodology

### Extraction
- Downloaded official PDFs from SEBI and RBI portals
- Scraped public datasets from Kaggle and ADB
- Extracted text content using PyPDF2 and pandas

### Cleaning
- Removed duplicate questions
- Standardized terminology (₹ for rupees, consistent date formats)
- Corrected grammatical errors
- Verified factual accuracy against official sources

### Synthesis
- Created question-answer pairs based on extracted content
- Ensured SEBI compliance (educational only, no specific investment advice)
- Added Hindi and Kannada translations for accessibility
- Incorporated real-world scenarios from household finance data

### Final Dataset Statistics
- **Total Samples:** 96 question-answer pairs
- **Languages:** English (primary), Hindi, Kannada
- **Topics Covered:** 12 major areas (Assets, Liabilities, Savings, EMI, Investments, Insurance, Banking, Loans, Tax, Real Estate, Gold, Retirement)
- **Average Question Length:** 47 characters
- **Average Answer Length:** 633 characters
- **Format:** CSV (UTF-8 encoding)

---

## Compliance and Ethics

### SEBI Guidelines Adherence
- All content is **educational** in nature
- No specific stock/mutual fund recommendations
- No guaranteed return promises
- Appropriate risk disclosures included

### Data Privacy
- No personal identifiable information (PII) used
- Only aggregated and anonymized data from public sources
- Compliant with IT Act 2000 and Digital Personal Data Protection Act 2023

### Accessibility
- Multilingual support (English, Hindi, Kannada)
- Simple language for financially illiterate users
- Voice input/output for accessibility

---

## Dataset Availability

**Project Dataset:** `datasets/comprehensive_financial_literacy.csv`

**Contents:**
- Column 1: `input` (questions)
- Column 2: `output` (answers)
- Encoding: UTF-8 with BOM
- Format: CSV

**License:** Educational use only (as per source licenses)

---

## Contact and Verification

For verification of sources or methodology:
- SEBI Toll-Free: 1800-22-7575
- RBI Toll-Free: 1800-425-1492
- NCFE Website: https://ncfe.org.in/contact-us/

---

**Last Updated:** October 7, 2025
**Project:** FinLit AI - Financial Literacy Assistant
**Developer:** [Your Name]
**Institution:** [Your College]
