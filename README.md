PDF Number Extractor

Overview

This Python script extracts and identifies the largest number from a PDF document using natural language processing and regular expressions. It performs two key tasks:

1) Finds the largest number while considering natural language scaling (e.g., "5 million" → 5,000,000).

2) Finds the largest raw numerical value without considering context (e.g., "9999" is greater than "5 million").

Getting Started

Prerequisites
* Python 3 
* PyMuPDF 

Installing 
* The only dependency required is PyMuPDF
  * pip install PyMuPDF

Usage: 
1) Clone the repository
   * git clone https://github.com/NFrosticles/find-largest-number-in-a-pdf.git
1) Update the file path in the script to point to your PDF: 
   * pdf_file_path = "C:\\Your\\Path\\Here\\filename.pdf"
3) Run the script from your terminal or command prompt
