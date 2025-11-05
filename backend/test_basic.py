#!/usr/bin/env python3
"""
Basic test script to verify backend setup
Run this after installation to check if everything is working
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")

    try:
        import flask
        print("✓ Flask imported successfully")
    except ImportError as e:
        print(f"✗ Flask import failed: {e}")
        return False

    try:
        import chromadb
        print("✓ ChromaDB imported successfully")
    except ImportError as e:
        print(f"✗ ChromaDB import failed: {e}")
        return False

    try:
        from sentence_transformers import SentenceTransformer
        print("✓ SentenceTransformers imported successfully")
    except ImportError as e:
        print(f"✗ SentenceTransformers import failed: {e}")
        return False

    try:
        from openai import OpenAI
        print("✓ OpenAI library imported successfully")
    except ImportError as e:
        print(f"✗ OpenAI library import failed: {e}")
        return False

    try:
        import cv2
        print("✓ OpenCV imported successfully")
    except ImportError as e:
        print(f"✗ OpenCV import failed: {e}")
        return False

    try:
        from PIL import Image
        print("✓ Pillow imported successfully")
    except ImportError as e:
        print(f"✗ Pillow import failed: {e}")
        return False

    return True


def test_environment():
    """Test if environment variables are set"""
    print("\nTesting environment variables...")

    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv('OPENROUTER_API_KEY')

    if api_key:
        print(f"✓ OPENROUTER_API_KEY is set (length: {len(api_key)})")
    else:
        print("⚠ OPENROUTER_API_KEY is not set in .env file")
        print("  You'll need to add it before using LLM features")

    return True


def test_directories():
    """Test if required directories exist"""
    print("\nTesting directories...")

    dirs = [
        'app/static/uploads',
        'app/static/generated',
        'data/chroma_db'
    ]

    all_exist = True
    for dir_path in dirs:
        if os.path.exists(dir_path):
            print(f"✓ {dir_path} exists")
        else:
            print(f"✗ {dir_path} does not exist")
            print(f"  Creating: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
            all_exist = False

    return True


def test_app_creation():
    """Test if Flask app can be created"""
    print("\nTesting Flask app creation...")

    try:
        from app import create_app
        app = create_app('development')
        print("✓ Flask app created successfully")

        # Test routes
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✓ Root endpoint responds correctly")
            else:
                print(f"✗ Root endpoint returned status {response.status_code}")
                return False

            response = client.get('/health')
            if response.status_code == 200:
                print("✓ Health endpoint responds correctly")
            else:
                print(f"✗ Health endpoint returned status {response.status_code}")
                return False

        return True

    except Exception as e:
        print(f"✗ Flask app creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Wardrobe AI Backend - Setup Verification")
    print("=" * 60)

    results = []

    results.append(("Imports", test_imports()))
    results.append(("Environment", test_environment()))
    results.append(("Directories", test_directories()))
    results.append(("App Creation", test_app_creation()))

    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)

    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:20} {status}")
        if not passed:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n🎉 All tests passed! Backend is ready to use.")
        print("\nNext steps:")
        print("1. Make sure OPENROUTER_API_KEY is set in .env")
        print("2. Run: python run.py")
        print("3. Visit: http://localhost:5000")
        return 0
    else:
        print("\n⚠ Some tests failed. Please fix the issues above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
