# henrycoeff

## Features
Allows the computation of Henry coefficient in the units of [mol/m3/Pa] directly from
the sim.log output file of Brick-CFCMC
  

## Installation
You can install this package locally by cloning the repository and using `pip`:

```bash
git clone [https://github.com/tijinsaji/compiledUdl.git](https://github.com/tijinsaji/compiledUdl.git)

cd compiledUdl

pip install -r requirements.txt .
```


## Usage
Go to the directory which contains the $\lambda$ directories and do
```python
import compiledUdl

compiledUdl.main()
```
