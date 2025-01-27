import PyInstaller.__main__
import os
import shutil

def clean_directories():
    """Clean build and dist directories"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name} directory...")
            shutil.rmtree(dir_name)

def build_executable():
    """Build the executable using the spec file"""
    print("Building executable...")
    PyInstaller.__main__.run([
        'NVDA_TSM_Ratio_Chart.spec',
        '--clean'  # Clean PyInstaller cache
    ])

def setup_distribution():
    """Setup the distribution folder"""
    dist_dir = 'dist'
    if os.path.exists(dist_dir):
        # Copy README to dist directory
        shutil.copy2('README.txt', os.path.join(dist_dir, 'README.txt'))
        print("\nDistribution setup complete!")
        print(f"\nExecutable and files can be found in the '{dist_dir}' directory:")
        print("- NVDA_TSM_Ratio_Chart.exe")
        print("- README.txt")
    else:
        print("\nError: Build failed - dist directory not found")

if __name__ == "__main__":
    try:
        clean_directories()
        build_executable()
        setup_distribution()
    except Exception as e:
        print(f"\nError during build process: {str(e)}")
    else:
        print("\nBuild completed successfully!")
        print("\nTo distribute the application:")
        print("1. Share both files from the 'dist' directory")
        print("2. Users must have Interactive Brokers TWS/Gateway running")
        print("3. Double-click the exe to run the application")
