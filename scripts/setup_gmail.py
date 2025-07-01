import webbrowser
import os

def setup_gmail():
    print("\nSetting up Gmail for FixItHub Email Verification")
    print("===========================================")
    
    # Step 1: Enable 2-Step Verification
    print("\nStep 1: Enable 2-Step Verification")
    print("- Go to your Google Account: https://myaccount.google.com/security")
    print("- Under '2-Step Verification', click 'Turn on 2-Step Verification'")
    print("- Follow the steps to set up 2-Step Verification")
    
    # Step 2: Generate App Password
    print("\nStep 2: Generate App Password")
    print("- Go to App Passwords page: https://myaccount.google.com/apppasswords")
    print("- Select 'Mail' as the app")
    print("- Select 'Other (Custom name)' and name it 'FixItHub'")
    print("- Copy the 16-character password that appears")
    
    # Step 3: Update .env file
    print("\nStep 3: Update .env file")
    print("Create a .env file in your project root with the following content:")
    print("""
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=noreply@fixithub.com
FRONTEND_URL=http://127.0.0.1:8000
""")
    
    # Open Google Account security page
    print("\nOpening Google Account security page...")
    webbrowser.open("https://myaccount.google.com/security")
    
    print("\nAfter completing the steps:")
    print("1. Replace 'your-email@gmail.com' with your Gmail address")
    print("2. Replace 'your-app-specific-password' with the 16-character app password")
    print("3. Save the .env file")
    print("4. Restart the Django server")
    
    print("\nNote: Never commit the .env file to version control")
    print("Add '.env' to your .gitignore file if it's not already there")

if __name__ == "__main__":
    setup_gmail()
