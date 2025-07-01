import os
import sys
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def test_signup_and_verification():
    print("\nTesting Signup and Email Verification")
    print("====================================")
    
    # Get the frontend URL from environment or default to localhost
    frontend_url = os.getenv('FRONTEND_URL', 'http://127.0.0.1:8000')
    
    # Start the browser
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    try:
        # Test 1: Navigate to signup page
        print("\nTest 1: Navigate to signup page")
        driver.get(f"{frontend_url}/signup/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_full_name"))
        )
        print("✓ Test 1 passed: Signup page loaded successfully")
        
        # Test 2: Fill out signup form
        print("\nTest 2: Fill out signup form")
        full_name = "Test User"
        email = "testuser@example.com"
        password = "TestPassword123!"
        
        driver.find_element(By.ID, "id_full_name").send_keys(full_name)
        driver.find_element(By.ID, "id_email").send_keys(email)
        driver.find_element(By.ID, "id_password").send_keys(password)
        
        # Submit the form
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        
        # Wait for success message
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )
        print("✓ Test 2 passed: Signup successful")
        
        # Test 3: Check email (we'll simulate this since we can't actually check email)
        print("\nTest 3: Simulating email check")
        print("Please check your email inbox for the verification email.")
        print("The email should contain a verification link.")
        
        # Wait for user to check email
        input("Press Enter after checking your email...")
        
        # Test 4: Verify email
        print("\nTest 4: Verify email")
        driver.get(f"{frontend_url}/login/")
        
        # Enter email and password
        driver.find_element(By.ID, "id_email").send_keys(email)
        driver.find_element(By.ID, "id_password").send_keys(password)
        
        # Click login
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        
        # Wait for login success
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
            )
            print("✓ Test 4 passed: Login successful")
        except:
            print("✗ Test 4 failed: Login failed - email may not be verified")
            
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    test_signup_and_verification()
