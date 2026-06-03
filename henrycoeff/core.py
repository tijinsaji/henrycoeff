import re
import os
import numpy as np

def parse_volume(logfile):
    """
    Return the first numeric value on the 2nd line that starts with 'Volume'.
    Ignores lines like 'Partial Molar Volume'.
    """
    vol_count = 0
    with open(logfile, "r") as f:
        for raw in f:
            line = raw.strip()
            if line.startswith("Volume") and not line.startswith("Volume of"):
                if line == "Partial Molar Volume" or "Partial Molar Volume" in line:
                    continue
                vol_count += 1
                if vol_count == 2:
                    nums = re.findall(r'[+-]?\d+(?:\.\d+)?(?:[Ee][+-]?\d+)?', line)
                    return float(nums[0]) if nums else None
    return None

def parse_number_of_molecules_solvent(logfile, solvent_name):
    """
    Find the 'Number of molecules' section and read the target solvent row.
    Returns the first numeric value on that row.
    """
    in_section = False
    with open(logfile, "r") as f:
        for raw in f:
            line = raw.rstrip("\n")
            stripped = line.strip()
            if stripped.startswith("Number of molecules"):
                in_section = True
                continue

            if in_section:
                if (stripped == "" or
                    stripped.startswith(("#", "=", "-")) or
                    stripped.lower().startswith(("mole fractions", "configuration", "forcefield",
                                                "topology", "simulation", "partial molar volume"))):
                    in_section = False
                    continue

                m = re.match(r'^\s*'+solvent_name+r'(\s+)([+-]?\d+(?:\.\d+)?(?:[Ee][+-]?\d+)?)\b', line)
                if m:
                    val = float(m.group(2))
                    return int(val) if abs(val - int(val)) < 1e-9 else val
    return None

def parse_excess_frac_mol(logfile, frac_mol):
    """
    Find the last line starting with 'Total [frac_mol]' and extract the number after 'Excess'.
    """
    in_section = False
    with open(logfile, "r") as f:
        for raw in f:
            line = raw.rstrip("\n")
            stripped = line.strip()
            
            section_head_word = "Total" + " " + frac_mol 
            if stripped.startswith(section_head_word):
                in_section = True
                continue

            if in_section:
                if (stripped == "" or
                    stripped.startswith(("#", "=", "-")) or
                    stripped.lower().startswith(("mole fractions", "configuration", "forcefield",
                                                "topology", "simulation", "partial molar volume"))):
                    in_section = False
                    continue

                m = re.match(r'^\s*Excess(\s+)([+-]?\d+(?:\.\d+)?(?:[Ee][+-]?\d+)?)\b', line)
                if m:
                    val = float(m.group(2))
                    return int(val) if abs(val - int(val)) < 1e-9 else val
    return None

def get_temperature(settings_filepath):
    """Parses system temperature from settings input file."""
    with open(settings_filepath, "r") as f:
        lines = f.readlines()
    
    second_row = lines[1].split()
    temperature = float(second_row[1])
    return temperature

def compute_H_s_cp(T, num_solvent, volume_sim, mu_excess):
    """
    T - temperature of the system
    num_solvent - number of molecules of the solvent
    volume_sim - volume of simulation box in A-3
    mu_excess - excess chemical potential of solute in K
    """
    kb = 1.38 * 1e-23  # J/K
    volume = volume_sim * 1e-30  # volume in m-3
    rho_solvent = num_solvent / volume  # Number density of solvent in m-3

    K_px = rho_solvent * kb * T * np.exp(mu_excess / T)  # Henry volatility coefficient in Pa

    rho_H2O = 1000   # in kg/m3; Mass density of water
    M_H2O = 18 * 1e-3  # in kg/mol; Molar mass of water

    H_s_cp = rho_H2O / (M_H2O * K_px)  # Henry coefficient in mol/(m3 Pa)
    return H_s_cp