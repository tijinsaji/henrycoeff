import sys
import os
from .core import (
    parse_volume, 
    parse_number_of_molecules_solvent, 
    parse_excess_frac_mol, 
    get_temperature, 
    compute_H_s_cp
)

__version__ = "0.1.0"

def main():
    """
    Execution script matching original terminal arguments.
    Expects directory pathway as an input command.
    """
    '''if len(sys.argv) < 2:
        print("Error: Missing target directory pathway argument.")
        print("Usage: henrycoef /path/to/simulation/directory")
        sys.exit(1)'''

    solvent_name = input("Enter the name of the solvent: ")
    solvent_name = sys.argv[1]
    fractional_molecule = input("Enter the display name of fractional molecule: ")
    fractional_molecule = sys.argv[2]

    current_directory = input("Enter the current directory path where sim.log is located: ")
    current_directory = sys.argv[3] 
    logfile = os.path.join(current_directory, "sim.log") 
    settings_filepath = os.path.join(current_directory, "INPUT/settings.in") 
    
    if not os.path.exists(logfile):
        print(f"Error: Logfile not found at {logfile}")
        sys.exit(1)
        
    if not os.path.exists(settings_filepath):
        print(f"Error: Settings file not found at {settings_filepath}")
        sys.exit(1)

    try:
        volume = parse_volume(logfile)
        num_solvent = parse_number_of_molecules_solvent(logfile, solvent_name)
        excess_frac_mol = parse_excess_frac_mol(logfile, fractional_molecule)
        temperature = get_temperature(settings_filepath)
        
        H_s_cp = compute_H_s_cp(temperature, num_solvent, volume, excess_frac_mol)
        print(H_s_cp)
    except Exception as e:
        print(f"Execution Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()