from functions.get_files_info import get_files_info
from functions.get_files_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

def run_tests():
    # Test current directory
    print("\nResult for current directory:")
    result = get_files_info("calculator", ".")
    print(result)

    # Test pkg subdirectory
    print("\nResult for 'pkg' directory:")
    result = get_files_info("calculator", "pkg")
    print(result)

    # Test /bin directory (should fail)
    print("\nResult for '/bin' directory:")
    result = get_files_info("calculator", "/bin")
    print(result)

    # Test parent directory (should fail)
    print("\nResult for '../' directory:")
    result = get_files_info("calculator", "../")
    print(result)

    # Test file contents
    print("\nResult for 'main.py' content:")
    result = get_file_content("calculator", "main.py")
    print(result)

    print("\nResult for 'pkg/calculator.py' content:")
    result = get_file_content("calculator", "pkg/calculator.py")
    print(result)

    print("\nResult for '/bin/cat' content (should fail):")
    result = get_file_content("calculator", "/bin/cat")
    print(result)

    print("\nResult for non-existent file:")
    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(result)

    # Test writing to a file in root directory
    print("\nResult for writing to 'lorem.txt':")
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result)

    # Test writing to a file in subdirectory
    print("\nResult for writing to 'pkg/morelorem.txt':")
    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result)

    # Test writing to a file outside working directory (should fail)
    print("\nResult for writing to '/tmp/temp.txt':")
    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(result)

    # Test running Python files
    print("\nRunning main.py (no args):")
    result = run_python_file("calculator", "main.py")
    print(result)

    print("\nRunning main.py with calculation:")
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result)

    print("\nRunning tests.py:")
    result = run_python_file("calculator", "tests.py")
    print(result)

    print("\nTrying to run file outside working directory:")
    result = run_python_file("calculator", "../main.py")
    print(result)

    print("\nTrying to run nonexistent file:")
    result = run_python_file("calculator", "nonexistent.py")
    print(result)

if __name__ == "__main__":
    run_tests()