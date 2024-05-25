# GMExtensionBase

> Template for GameMaker extensions using the "Runner Interface Extension" option

Uses code that originates from <https://github.com/YoYoGames/GMEXT-Steamworks>
(commit `eff5b8d2f53513c27819dcd17186662926ca1d85`), which is available under
the Apache 2.0 License.

## Building

> Requires [CMake](https://cmake.org) version 3.23 or newer!

```sh
git clone https://github.com/blueburncz/GMExtensionBase.git
cd GMExtensionBase
mkdir build
cd build
cmake ..
cmake --build . --config=Release
```

The last command also copies the dynamic library into the extensions folder,
so you don't have to do that by hand.

## Injecting functions and JSDoc into extension.yy file

> Requires [Python 3](https://www.python.org/downloads/)!

```sh
python.exe -m venv env
./env/scripts/activate
pip install -r requirements.txt
python.exe ./inject-docs.py
deactivate
```
