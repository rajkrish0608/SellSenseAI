"""
Test Setup Script
Verifies all dependencies and configuration
"""

import sys
import os

def test_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} (need 3.8+)")
        return False


def test_imports():
    """Test if all required packages are installed"""
    print("\n📦 Testing package imports...")
    
    packages = [
        ('flask', 'Flask'),
        ('flask_sqlalchemy', 'Flask-SQLAlchemy'),
        ('flask_login', 'Flask-Login'),
        ('werkzeug', 'Werkzeug'),
        ('google.generativeai', 'google-generativeai'),
        ('requests', 'requests'),
        ('dotenv', 'python-dotenv'),
    ]
    
    all_ok = True
    for module, name in packages:
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} - NOT INSTALLED")
            all_ok = False
    
    return all_ok


def test_env_file():
    """Check .env file"""
    print("\n🔐 Checking .env file...")
    
    if not os.path.exists('.env'):
        print("   ❌ .env file not found")
        return False
    
    print("   ✅ .env file exists")
    
    # Check for required variables
    with open('.env', 'r') as f:
        content = f.read()
    
    required = ['GOOGLE_GEMINI_API_KEY', 'SECRET_KEY']
    missing = []
    
    for var in required:
        if var not in content:
            missing.append(var)
        elif f"{var}=" in content and (f"{var}=$" in content or f"{var}= " in content or "your-" in content or "change-this" in content):
            print(f"   ⚠️  {var} needs to be configured")
        else:
            print(f"   ✅ {var} configured")
    
    if missing:
        print(f"   ❌ Missing: {', '.join(missing)}")
        return False
    
    return True


def test_directories():
    """Check directory structure"""
    print("\n📁 Checking directory structure...")
    
    required_dirs = [
        'ai_services',
        'api',
        'database',
        'static/css',
        'static/generated_assets',
        'templates',
    ]
    
    all_ok = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"   ✅ {dir_path}")
        else:
            print(f"   ❌ {dir_path} - MISSING")
            all_ok = False
    
    return all_ok


def test_files():
    """Check critical files"""
    print("\n📄 Checking critical files...")
    
    required_files = [
        'app.py',
        'config.py',
        'requirements.txt',
        '.gitignore',
        'ai_services/__init__.py',
        'ai_services/gemini_ai.py',
        'ai_services/simple_image_gen.py',
        'database/models.py',
        'api/__init__.py',
        'templates/base.html',
        'static/css/modern-dark.css',
    ]
    
    all_ok = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - MISSING")
            all_ok = False
    
    return all_ok


def test_database():
    """Test database initialization"""
    print("\n🗄️  Testing database...")
    
    try:
        from app import app, db
        with app.app_context():
            db.create_all()
        print("   ✅ Database can be initialized")
        return True
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 AGENTIC SALES AI - SETUP VERIFICATION")
    print("="*70)
    
    results = {
        'Python Version': test_python_version(),
        'Package Imports': test_imports(),
        'Environment File': test_env_file(),
        'Directory Structure': test_directories(),
        'Critical Files': test_files(),
        'Database': test_database(),
    }
    
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:.<50} {status}")
        if not passed:
            all_passed = False
    
    print("="*70)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n✅ Your application is ready to run!")
        print("\nStart with: ./run.sh (or run.bat on Windows)")
        print("Open: http://localhost:5000")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("\nPlease fix the issues above before running the application.")
        print("\nRun setup again: ./setup.sh (or setup.bat on Windows)")
    
    print("\n")
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())