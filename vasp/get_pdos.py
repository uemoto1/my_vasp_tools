#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import numpy as np
import sys
import os

tree = ET.parse('vasprun.xml')
root = tree.getroot()

ISPIN = int(root.find(".//i[@name='ISPIN']").text)
print("# ISPIN = %s" % ISPIN)

NBANDS = int(root.find(".//i[@name='NBANDS']").text)
print("# NBANDS = %d" % NBANDS)

NEDOS = int(root.find(".//i[@name='NEDOS']").text)
print("# NEDOS=%d" % NEDOS)

natom = int(root.find(".//atoms").text)
print("# natom=%d" % natom)

efermi = float(root.find(".//i[@name='efermi']").text)
print("# efermi=%f" % efermi)

elem_array = root.find("./calculation/dos/partial/array")

field = []
for item in elem_array.findall("./field"):
    field.append(item.text)
nfield = len(field)

if not os.path.isdir("pdos"):
    os.mkdir("pdos")

elem_set = elem_array.find("./set")
for jion in range(natom):
    elem_set_ion = elem_set.find("./set[@comment='ion %d']" % (jion+1))
    for js in range(ISPIN):
        elem_set_spin = elem_set_ion.find("./set[@comment='spin %d']" % (js+1))
        with open("pdos/ion%03d_spin%d.txt" % (jion+1, js+1), "w") as fh:
            print(fh.name)
            fh.write("#" + " ".join(field) + "\n")
            for r in elem_set_spin:
                fh.write(r.text + "\n")

dat = np.empty([natom, ISPIN, NEDOS, nfield])

for jion in range(natom):
    for js in range(ISPIN):
        dat[jion, js, :, :] = np.loadtxt("pdos/ion%03d_spin%d.txt" % (jion+1, js+1))

if not os.path.isdir("pdos_orbit_ef0"):
    os.mkdir("pdos_orbit_ef0")

tmp = np.empty([NEDOS, 2])
for jion in range(natom):
    for ifield in range(1, nfield):
        for js in range(ISPIN):
            tmp[:, 0] = dat[jion, js, :, 0] - efermi
            tmp[:, 1] = dat[jion, js, :, ifield]
            name = "pdos_orbit_ef0/ion%03d_%s_spin%d.txt" % (jion+1, field[ifield].strip(), js+1)
            print(name)
            np.savetxt(name, tmp, header="Energy-E_F[eV] PDoS[1/eV]")
            
# # Export pdos data
# buff = np.zeros([NEDOS, ISPIN+1])
# for iion1 in range(1, natom+1):
#     for ifield in range(1, nfield):
#         tag = elem_field[ifield].text.replace(" ", "")
#         name = "pdos%03d_%s.txt" % (iion1, tag)
#         buff[:, 0] = pdos[0, 0, :, 0]
#         for iISPIN in range(1, ISPIN):
#             buff[:, iISPIN] = pdos[iISPIN-1, iion1-1, :, ifield]
#         np.savetxt(name, buff, 
#             header="Energy-EF[eV] DoS[1/eV]", fmt="%+12.6e")
#         print("# Generated %s" % name)
        




