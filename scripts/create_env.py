def create_env_file():
    env_content = """
# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=noreply@fixithub.com

# Frontend URL
FRONTEND_URL=http://127.0.0.1:8000
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print(".env file created successfully!")
    print("Please update the following values:")
    print("1. Replace 'your-email@gmail.com' with your Gmail address")
    print("2. Replace 'your-app-specific-password' with the 16-character app password")

if __name__ == "__main__":
    create_env_file()
