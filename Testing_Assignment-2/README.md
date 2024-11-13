This project contains automated test scripts for testing various functionalities of a web application using Selenium

## Prerequisites

- Java Development Kit (JDK) 8 or higher
- Google Chrome and ChromeDriver
- Visual Studio Code or any other IDE

## Installation

1. **Install WebDriver**
    Selenium requires browser-specific drivers:
    Chrome: Download ChromeDriver
    Link: https://developer.chrome.com/docs/chromedriver/downloads
    Firefox: Download GeckoDriver

2. **Install Selenium in your Python/Java Project**
    If using Python: pip install selenium

    If using Maven for Java, add the following to your pom.xml:
    <dependency>
    <groupId>org.seleniumhq.selenium</groupId>
    <artifactId>selenium-java</artifactId>
    <version>4.0.0</version>
    </dependency>

    Add the WebDriver to your system path or specify its location in the test script.

3. **Install Necessary Extensions in VS Code**
    Java Extension Pack: This includes essential extensions for Java development.
    Maven for Java: Helps with managing Maven projects.
    TestNG: If you are using TestNG for your tests.

## Open Your Project in VS Code

1. **Clone the Repository**
   
   git clone https://github.com/Shura-VG/Selenium_Testing.git
   cd Selenium_Testing

2. **Open the Project**
    Open VS Code.
    Go to File > Open Folder and select your project folder.

## Run your test

1. Open the integrated terminal in VS Code (Ctrl + Shift + ` ).
2. Run the test using : pytest "yourfile.py"

## View Test Results

Test results will be displayed in the terminal.

## Generate HTML Report

To generate an HTML report using pytest (if applicable):

1. Ensure pytest and pytest-html are installed:

    pip install pytest pytest-html

2. Run pytest with the HTML report option:

    pytest --html=report.html

The report file will be in your project folder. You can open it with your browser to see.

## Summary

By following these steps, you can set up and run your Selenium tests using VS Code. This setup ensures you can manage your project, write and execute tests, and view results all within the same environment. If you have any other questions or need further assistance, please feel free to ask!
