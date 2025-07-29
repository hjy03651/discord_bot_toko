#!/usr/bin/env python3
"""
Manual test script for DBreconnection command
This script shows how to manually test the /dbreconnect command
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from DBclass import Databases

# Load environment variables
load_dotenv()


def test_current_connection():
    """Test if current database connection works"""
    print("Testing current database connection...")
    try:
        db = Databases()
        # Try a simple query
        db.cursor.execute("SELECT 1")
        result = db.cursor.fetchone()
        if result and result[0] == 1:
            print("✅ Current database connection is working!")
            return True
        else:
            print("❌ Database query returned unexpected result")
            return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    finally:
        try:
            db.__del__()
        except:
            pass


def test_connection_with_wrong_credentials():
    """Test what happens with wrong credentials"""
    print("\nTesting connection with invalid credentials...")

    # Save original values
    original_host = os.getenv("DB_HOST")

    # Set invalid host
    os.environ["DB_HOST"] = "invalid_host_that_does_not_exist"

    try:
        db = Databases()
        print("❌ Connection succeeded with invalid host (this shouldn't happen)")
        return False
    except Exception as e:
        print(f"✅ Connection failed as expected: {type(e).__name__}")
        return True
    finally:
        # Restore original value
        if original_host:
            os.environ["DB_HOST"] = original_host


def simulate_dbreconnect_scenarios():
    """Simulate different scenarios the /dbreconnect command might encounter"""
    print("\n" + "=" * 60)
    print("Simulating /dbreconnect command scenarios")
    print("=" * 60)

    print("\n1. Normal operation - database is accessible:")
    if test_current_connection():
        print("   → /dbreconnect should show: ✅ 데이터베이스 재연결 성공!")

    print("\n2. Database server is down or unreachable:")
    test_connection_with_wrong_credentials()
    print("   → /dbreconnect should show: 🐱 재연결 실패! 서버 관리자에게 문의하세요")

    print("\n3. After fixing connection issues:")
    if test_current_connection():
        print("   → /dbreconnect should reconnect successfully")


def print_test_instructions():
    """Print instructions for manual testing"""
    print("\n" + "=" * 60)
    print("Manual Testing Instructions for /dbreconnect")
    print("=" * 60)
    print("\n1. Start your Discord bot:")
    print("   python InuiBot130.py")

    print("\n2. In Discord, use the slash command:")
    print("   /dbreconnect")

    print("\n3. Expected behaviors:")
    print("   - Success: Shows ✅ with '데이터베이스 재연결 성공!' message")
    print(
        "   - Failure: Shows 🐱 with '재연결 실패! 서버 관리자에게 문의하세요' message"
    )
    print("   - The command updates all cogs with new database connections")

    print("\n4. To test error handling:")
    print("   - Stop your database server")
    print("   - Run /dbreconnect (should show error)")
    print("   - Start database server again")
    print("   - Run /dbreconnect (should succeed)")

    print("\n5. Check that other commands still work after reconnection:")
    print("   - Try any database-dependent commands like /sql or book-related commands")


def check_environment():
    """Check if environment is properly configured"""
    print("\n" + "=" * 60)
    print("Environment Check")
    print("=" * 60)

    required_vars = [
        "DB_HOST",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
        "DB_PORT",
        "DISCORD_TOKEN",
    ]

    all_good = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if var == "DB_PASSWORD" or var == "DISCORD_TOKEN":
                print(f"✅ {var}: ****** (hidden)")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")
            all_good = False

    if not all_good:
        print("\n⚠️  Some environment variables are missing!")
        print("   Create a .env file with all required variables.")

    return all_good


def main():
    """Run the manual test helper"""
    print("DBreconnection Manual Test Helper")
    print("=" * 60)

    # Check environment
    if not check_environment():
        print("\n❌ Please configure your environment before testing.")
        return

    # Run connection tests
    simulate_dbreconnect_scenarios()

    # Print manual testing instructions
    print_test_instructions()

    print("\n✨ Manual test helper completed!")


if __name__ == "__main__":
    main()
