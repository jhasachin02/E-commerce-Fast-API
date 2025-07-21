#!/usr/bin/env python3
"""
Comprehensive test runner for E-Commerce FastAPI Backend
Runs all tests and generates a detailed report
"""

import sys
import subprocess
import time
from pathlib import Path

def run_command(command, description):
    """Run a command and return the result"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            if result.stdout:
                print("Output:", result.stdout[:500])  # Limit output
        else:
            print(f"❌ {description} - FAILED")
            if result.stderr:
                print("Error:", result.stderr[:500])
                
        return result.returncode == 0, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT")
        return False, "", "Test timed out"
    except Exception as e:
        print(f"💥 {description} - ERROR: {str(e)}")
        return False, "", str(e)

def main():
    """Main test runner"""
    print("🧪 E-Commerce FastAPI Backend Test Suite")
    print("="*60)
    
    # Change to the project root directory
    project_root = Path(__file__).parent.parent
    print(f"Project root: {project_root}")
    
    test_results = []
    
    # Test categories with their respective commands
    tests = [
        ("python -m pytest tests/ -v", "Unit Tests"),
        ("python tests/test_mongodb.py", "MongoDB Connection Test"),
        ("python tests/test_local_app.py", "Local Application Test"),
        ("python tests/simple_mongodb_test.py", "Simple MongoDB Test"),
        ("python tests/test_render_deployment.py", "Deployment Test"),
        ("python tests/test_create_product.py", "Product Creation Test"),
        ("python tests/test_direct_functions.py", "Direct Function Test"),
    ]
    
    start_time = time.time()
    
    for command, description in tests:
        success, stdout, stderr = run_command(command, description)
        test_results.append({
            'test': description,
            'success': success,
            'output': stdout,
            'error': stderr
        })
    
    # Generate summary
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results if result['success'])
    failed_tests = total_tests - passed_tests
    
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: ✅ {passed_tests}")
    print(f"Failed: ❌ {failed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    print(f"Duration: {duration:.2f} seconds")
    
    # Detail failed tests
    if failed_tests > 0:
        print("\n❌ FAILED TESTS:")
        for result in test_results:
            if not result['success']:
                print(f"  - {result['test']}")
                if result['error']:
                    print(f"    Error: {result['error'][:200]}...")
    
    print("\n" + "="*60)
    print("🎯 Test run completed!")
    
    # Exit with error code if any tests failed
    if failed_tests > 0:
        sys.exit(1)
    else:
        print("🎉 All tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
