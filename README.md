# CentralPackageManagerConvert
A simple Python script to move .NET solutions to CentralPackageManagement. It just iterates through your .csproj files and picks the highest version for each package. It doesn't solve conflicts.

Just set these values and run the script:

```python
path = '{path to your solution folder}'     # the root of your project
template_path = 'template.xml'              # path to the template.xml, file included or make your own
cpm_output_file = 'Directory.Package.Props' # path where the Directory.Package.Props file will be created
```
