import os
import shutil
from subprocess import run

def clean_directories():
    """Clean output directory"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name} directory...")
            shutil.rmtree(dir_name)

def build_executable():
    """Build the executable using pyinstaller directly"""
    print("Building executable...")
    
    # Basic PyInstaller command without metadata
    cmd = [
        'pyinstaller',
        '--noconfirm',
        '--onefile',
        '--windowed',
        '--name', 'NVDA_TSM_Ratio_Chart',
        '--add-data', 'README.txt:.',  # Fixed separator to use : instead of ;
        '--collect-all', 'numpy',
        '--collect-all', 'pandas',
        '--collect-all', 'matplotlib',
        '--collect-all', 'pytz',
        '--collect-all', 'ib_insync',
        'stock_ratio_chart.py'
    ]
    
    try:
        run(cmd, check=True)
        
        # Copy README to dist directory
        if os.path.exists('dist'):
            shutil.copy2('README.txt', os.path.join('dist', 'README.txt'))
            print("\nBuild completed successfully!")
            print("\nFiles in dist directory:")
            print("- NVDA_TSM_Ratio_Chart.exe")
            print("- README.txt")
        else:
            print("\nError: Build failed - dist directory not found")
            
    except Exception as e:
        print(f"\nError running PyInstaller: {str(e)}")
        print("Try running this command directly:")
        print(" ".join(cmd))

if __name__ == "__main__":
    try:
        clean_directories()
        build_executable()
    except Exception as e:
        print(f"\nError during build process: {str(e)}")
    else:
        print("\nTo distribute the application:")
        print("1. Share both files from the 'dist' directory")
        print("2. Users must have Interactive Brokers TWS/Gateway running")
        print("3. Double-click the exe to run the application")
