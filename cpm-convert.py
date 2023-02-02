import glob
from pkg_resources import packaging
import xml.etree.ElementTree as ET

path = ''                                             # the root of your project
template_path = 'template.xml'                        # path to the template.xml, file included or make your own
cpm_output_file = path + '\\Directory.Packages.props' # path where the Directory.Packages.props file will be created
package_versions = {}

def read_versions_from_csproj_file(file_path):
  tree = ET.parse(file_path)
  root = tree.getroot()
  for item_group in root.findall('ItemGroup'):
    for package_reference in item_group.findall('PackageReference'):
      package_versions[package_reference.attrib['Include']] = package_reference.attrib['Version'] if package_reference.attrib['Include'] not in package_versions else get_highest_version(package_versions[package_reference.attrib['Include']], package_reference.attrib['Version'])

def get_highest_version(saved_version, read_version):
  return read_version if packaging.version.parse(read_version) > packaging.version.parse(saved_version) else saved_version

def delete_versions_from_csproj_file(file_path):
  tree = ET.parse(file_path, parser=ET.XMLParser(target=ET.TreeBuilder(insert_comments=True)))
  root = tree.getroot()
  found = False
  for item_group in root.findall('ItemGroup'):
    for package_reference in item_group.findall('PackageReference'):
      if 'Version' in package_reference.attrib:
        found = True
        del package_reference.attrib['Version']
  if found:
    tree.write(file_path)
    with open(file_path, "a", encoding='utf-8') as file:
      file.write("\n")

def write_versions_to_cpm_file(template_path, output_path):
  tree = ET.parse(template_path, parser=ET.XMLParser(target=ET.TreeBuilder(insert_comments=True)))
  root = tree.getroot()
  item_group = root.find('ItemGroup')
  for package in sorted(package_versions.keys(), key=str.casefold):
    package_version = ET.Element('PackageVersion', Include=package, Version=package_versions[package])
    item_group.append(package_version)
  ET.indent(tree, '  ')
  tree.write(output_path)
  with open(output_path, "a", encoding='utf-8') as file:
    file.write("\n")

for file_path in glob.glob(path + '\\**\\*.csproj', recursive=True):
  read_versions_from_csproj_file(file_path)
  delete_versions_from_csproj_file(file_path)

write_versions_to_cpm_file(template_path, cpm_output_file)
