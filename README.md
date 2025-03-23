PDF Number Extractor

Overview

This Python script extracts and identifies the largest number from a PDF document using natural language processing and regular expressions. It performs two key tasks:

1) Finds the largest number while considering natural language scaling (e.g., "5 million" → 5,000,000).

2) Finds the largest raw numerical value without considering context (e.g., "9999" is greater than "5 million").

Getting Started

Prerequisites
* Python 3 
* PyPDF2 

Installing 
* The only dependency required is PyPDF2
  * pip install PyPDF2

Usage: 
1) Update the file path in the script to point to your PDF: 
   2) pdf_file_path = "C:\\Your\\Path\\Here\\filename.pdf"
3) Run the script from your terminal or command prompt