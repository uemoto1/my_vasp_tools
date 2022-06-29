#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import numpy as np
import re
import sys

tree = ET.parse('vasprun.xml')

root = tree.getroot()

ispin = int(root.find(".//i[@name='ISPIN']").text)
print("# ispin=%d" % ispin)

nedos = float(root.find(".//i[@name='NEDOS']").text)
print("# nedos=%d" % nedos)

efermi = float(root.find(".//i[@name='efermi']").text)
print("# efermi=%f" % efermi)

data = np.zeros([nedos, 1+ispin])

element_set1 = root.find("calculation/dos/total/array/set")
for element_set_spin in element_set1:
    comment = element_set_spin.attrib["comment"]
    i = int(re.sub(r"spin\s*(\d+)", r"\1", comment))
    for n, r in enumerate(element_set_spin):
        tmp = r.text.split()
        data[n, 0] = float(tmp[0]) - efermi
        data[n, i] = float(tmp[1])

np.savetxt("tdos.txt", data, 
    header="Energy-EF[eV] DoS[1/eV]", fmt="%+12.6e")
print("# Generated tdos.txt")


element_field = root.findall("calculation/dos/partial/array/field")


sys.exit(-1)

header = "# Energy-EF"
for item in element_field[1:]:
    header += " " + item.text.strip()

element_set1 = root.find("calculation/dos/partial/array/set")
for element_set_ion in element_set1:
    comment = element_set_ion.attrib["comment"]
    iion = int(re.sub(r"ion\s*(\d+)", r"\1", comment))
    for element_set_spin in element_set_ion:
        comment = element_set_spin.attrib["comment"]
        ispin = int(re.sub(r"spin\s*(\d+)", r"\1", comment))
        with open("pdos%03d_spin%d.txt" % (iion, ispin), "w") as fh:
            fh.write(header + "\n") 
            for r in element_set_spin:
                tmp = r.text.split()
                energy = float(tmp[0]) - efermi
                fh.write("%+12.6f" % energy)
                for i in range(1, len(tmp)):
                    fh.write(" %10.3e" % float(tmp[i]))
                fh.write("\n")
        print("# generated %s" % fh.name)

