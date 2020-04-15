from conans import ConanFile, tools
import os

class QtchartsConan(ConanFile):
    name = "Qt5Charts"
    version = "5.12.7"
    license = "GPL-3"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Qtcharts here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"

    def requirements(self):
        self.requires("qt/{}@bincrafters/stable".format(self.version))

    def source(self):
        self.run("git clone https://github.com/qt/qtcharts.git -b {}".format(self.version))

    def build(self):
        self.run('conan install qt/{}@bincrafters/stable -g qmake'.format(self.version))

        tools.replace_in_file("qtcharts/qtcharts.pro", "load(qt_parts)",
        '''CONFIG += conan_basic_setup
           include(../conanbuildinfo.pri)
           load(qt_parts)''')

        with open("conanbuildinfo.pri") as search:
            for line in search:
                line = line.rstrip()
                if "CONAN_BINDIRS_QT" in line:
                    qt_path = line.split('"')[1]

        self.run("PATH={}:$PATH qmake \"CONFIG+=release\" qtcharts/qtcharts.pro".format(qt_path))
        self.run("make V=1 -j{}".format(tools.cpu_count()))

    def package(self):
        self.copy("*.h", dst="include", src="include")
        self.copy("*.h", dst="qtcharts/src/charts", src="qtcharts/src/charts")
        self.copy("Q*", dst="include", src="include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so*", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.cmake", dst="lib", src="lib")

    def package_info(self):
        self.cpp_info.libs = ["Qt5Charts"]

        self.cpp_info.builddirs.append("lib/cmake/Qt5Charts/Qt5ChartsConfig.cmake")
        self.cpp_info.build_modules.append("lib/cmake/Qt5Charts/Qt5ChartsConfigVersion.cmake")

