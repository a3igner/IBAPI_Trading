# Creating a GitHub Release

Follow these steps to create a new release with the Windows executable:

1. Build the executable:
```bash
python build_simple.py
```

2. Create a new release on GitHub:
   - Go to your repository on GitHub
   - Click on "Releases"
   - Click "Create a new release"
   - Click "Choose a tag" and create a new tag (e.g., v1.0.0)
   - Set the release title (e.g., "Version 1.0.0")
   - Add release notes describing the changes
   - Drag and drop or select these files:
     - dist/NVDA_TSM_Ratio_Chart.exe
     - dist/README.txt

3. Release notes template:
```
## NVDA/TSM Ratio Chart v1.0.0

### Installation
1. Download NVDA_TSM_Ratio_Chart.exe
2. Download README.txt for instructions
3. Make sure Interactive Brokers TWS/Gateway is running
4. Double-click the executable to run

### Requirements
- Interactive Brokers TWS or Gateway
- Market data subscriptions for NVDA and TSM

### Changes in this version
- Initial release
- Real-time ratio monitoring
- 100-minute historical data
- Auto-updates every 10 seconds
```

4. After creating the release:
   - The download badge in README.md will automatically update
   - Users can download directly from the Releases page
   - The latest release will be linked from the repository homepage

Remember to:
- Tag releases with semantic versioning (vX.Y.Z)
- Include both the executable and README.txt
- Test the downloaded files before marking as the latest release
