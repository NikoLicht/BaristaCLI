# ☕BaristaCLI 
A little quirky terminal coffee adventure game. In this game you use actions on objects in order to achieve that delicious virtual brew. Have fun and play around.

BaristaCLI includes a few differnt objects that each impement some different actions. Watch out for the grinder that thing is a beast. Make sure to check out the fridge as well.

![baristaCLI](https://github.com/user-attachments/assets/bab1f9bc-d1d2-4d37-87fc-4e2674fd02b4)

---

## Running BaristaCLI
Choose one of the following methods to run the game:

### Option #0: Run the Docker Container
Find the docker container [here](https://hub.docker.com/u/artmole)
Make sure to run it as an interactive terminal like this (but with the correct version):
```sh
docker run -it docker run -it artmole/barista_cli:0.2
```

### Option #1: Run the Executable
Simply run the latest **.exe file** located in the [Executables folder](https://github.com/NikoLicht/BaristaCLI/tree/main/Executables).

### Option #2: Run with Python
If you prefer running the game via Python, follow these steps:
```sh
# Clone the repository
git clone https://github.com/NikoLicht/BaristaCLI.git
cd BaristaCLI

# Set up a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
venv\scripts\activate
# Mac / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python barista.py

# Exit the virtual environment
deactivate
```
### Option #3: Build it yourself
For those who want to build the project manually, a build.ps1 script is provided.
```sh
# Clone the repository
git clone https://github.com/NikoLicht/BaristaCLI.git
cd BaristaCLI

# Run the build script
./build.ps1
```

_Enjoy brewing your virtual coffee adventure with BaristaCLI! ☕_
