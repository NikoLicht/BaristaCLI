# BaristaCLI
A little quirky terminal coffee adventure game. In this game you use actions on objects in order to achieve that delicious virtual brew. Have fun and play around.

BaristaCLI includes a few differnt objects that each impement some different actions. Watch out for the grinder that thing is a beast. Make sure to check out the fridge as well.

![baristaCLI](https://github.com/user-attachments/assets/bab1f9bc-d1d2-4d37-87fc-4e2674fd02b4)


# Running BaristaCLI?

**You can run the (probably) outdated .exe** file in the executables folder

For the lazy: [BaristaCLI.exe](https://github.com/NikoLicht/BaristaCLI/blob/main/Executables/BaristaCLI_v_01.exe)

**Get your hands dirty** by running it with python
```sh
git clone https://github.com/NikoLicht/BaristaCLI.git
cd BaristaCLI
python -m venv venv
Windows: venv\scripts\activate OR Mac / Linux: source venv/bin/activate
pip install -r requirements.txt
python barista.py

deactivate (to exit your virtual evnironment)
```

Or alternatively **build it yourself**. I've added a build.ps1 script for building in PowerShell. Then you should get an executable that works on your system. Enjoy.
```sh
git clone https://github.com/NikoLicht/BaristaCLI.git
cd BaristaCLI
./build.ps1
```

# Prerequisites for building
1. Git, Python
2. Build tool / terminal
    * Windows: Enable PowerShell execution.
    * Linux / Mac: The same, but maybe use pwsh instead of PowerShell? I think maybe there is PowerShell available for Linux/Mac.
