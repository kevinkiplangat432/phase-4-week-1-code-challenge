import subprocess
import sys

def setup_mail_testing():
    """Setup local SMTP server for email testing"""
    print("Setting up email testing environment...")
    print("\nOption 1: Configure real email in .env file")
    print("Option 2: Use local SMTP server for testing")
    
    choice = input("\nChoose option (1 or 2): ").strip()
    
    if choice == "1":
        print("\nPlease update your .env file with:")
        print("""
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
        """)
        
    elif choice == "2":
        print("\nStarting local SMTP server on port 1025...")
        print("Emails will be printed to console instead of being sent.")
        
        # Update .env for local testing
        with open('.env', 'a') as f:
            f.write('\n# Local email testing\n')
            f.write('MAIL_SERVER=localhost\n')
            f.write('MAIL_PORT=1025\n')
            f.write('MAIL_USE_TLS=False\n')
            f.write('MAIL_USE_SSL=False\n')
        
        print("\nUpdated .env file for local testing.")
        print("\nIn a separate terminal, run:")
        print("python -m smtpd -n -c DebuggingServer localhost:1025")
        print("\nThen test email endpoints in your main terminal.")
    
    else:
        print("Invalid choice. Please run setup again.")

if __name__ == "__main__":
    setup_mail_testing()