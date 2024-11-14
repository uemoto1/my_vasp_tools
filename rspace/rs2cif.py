#!/usr/bin/env python3

bohr_aa = 0.529177
tbl = [
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
    "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", 
    "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", 
    "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", 
    "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", 
    "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn"
]

def float_fortran(x):
    return float(x.replace("d", "e").replace("D", "E"))

with open("parameters.inp") as fh:
    for line in fh:
        tmp1 = line.split("!")
        tmp2 = tmp1[0].split("=")
        if len(tmp2) >= 2:
            lhs = tmp2[0].strip()
            rhs = tmp2[1].strip()
            if lhs.lower() == "xmax":
                xmax = float_fortran(rhs)
            if lhs.lower() == "ymax":
                ymax = float_fortran(rhs)
            if lhs.lower() == "zmax":
                zmax = float_fortran(rhs)
            if lhs.lower() == "natom":
                natom = int(rhs)

with open("atom.xyz") as fh:
    header = fh.readline()
    atom_coord_list = []
    for i in range(natom):
        tmp = fh.readline().split()
        x = float_fortran(tmp[0])
        y = float_fortran(tmp[1])
        z = float_fortran(tmp[2])
        iz = int(int(tmp[3]))
        atom_coord_list.append([x, y, z, iz])


template = """
data_
_symmetry_space_group_name_H-M 'P 1'
_cell_length_a {A:.6f}
_cell_length_b {B:.6f}
_cell_length_c {C:.6f}
_cell_angle_alpha 90.0
_cell_angle_beta 90.0
_cell_angle_gamma 90.0
loop_
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
{ATOMIC_POSITION}
"""

with open("structure.cif", "w") as fh:
    fh.write(template.format(
        A=2*xmax*0.529177,
        B=2*ymax*0.529177,
        C=2*zmax*0.529177,
        ATOMIC_POSITION="\n".join([
            ("%s %.3f %.3f %.3f" % (tbl[iz-1], x/(2*xmax)+0.5, y/(2*ymax)+0.5, z/(2*zmax)+0.5))
            for (x, y, z, iz) in atom_coord_list
        ])
    ))


