# =======================================================
# CHOIX DU COMPILATEUR
# =======================================================

CXX = g++-15

# =======================================================
# ORGANISATION DES DOSSIERS
# =======================================================

DIR_SRC = src
DIR_OBJ = build
DIR_SETUPS = setups
DIR_NUMERICS = $(DIR_SRC)/numerics
DIR_PHYSICS = $(DIR_SRC)/physics
DIR_IO = $(DIR_SRC)/io

# =======================================================
# INFORMATIONS GÉNÉRALES SUR LA COMPILATION
# =======================================================

TARGET = main

# =======================================================
# DÉTECTION AUTOMATIQUE DES FLAGS MPI
# =======================================================

SHOW_MPI := $(shell mpicxx --showme:compile) $(shell mpicxx --showme:link)
CFLAGS_MPI := $(shell printf '%s\n' "$(SHOW_MPI)" | tr ' ' '\n' | grep '^-I')
LFLAGS_MPI := $(shell printf '%s\n' "$(SHOW_MPI)" | tr ' ' '\n' | grep '^-L')
LIBS_MPI := $(shell printf '%s\n' "$(SHOW_MPI)" | tr ' ' '\n' | grep '^-l')
LIBDIR_MPI := $(shell printf '%s\n' "$(SHOW_MPI)" | tr ' ' '\n' | grep '^-L' | head -n1 | sed 's/^-L//')

# =======================================================
# DÉTECTION AUTOMATIQUE DES FLAGS HDF5
# =======================================================

SHOW_HDF5 := $(shell h5c++ -show)
CFLAGS_HDF5 := $(shell printf '%s\n' "$(SHOW_HDF5)" | tr ' ' '\n' | grep '^-I')
LFLAGS_HDF5 := $(shell printf '%s\n' "$(SHOW_HDF5)" | tr ' ' '\n' | grep '^-L')
LIBS_HDF5 := $(shell printf '%s\n' "$(SHOW_HDF5)" | tr ' ' '\n' | grep -E '^-l|^/.+\.(a|so|so\.[0-9.]+|dylib)$$')
LIBDIR_HDF5 := $(shell printf '%s\n' "$(SHOW_HDF5)" | tr ' ' '\n' | grep '^-L' | head -n1 | sed 's/^-L//')

# =======================================================
# OPTIONS DE COMPILATION
# =======================================================

CXXFLAGS = -O3 \
           -std=c++20 \
           -fopenmp \
		   -I$(DIR_SRC) \
		   -I$(DIR_SETUPS) \
		   -I$(DIR_NUMERICS) \
		   -I$(DIR_PHYSICS) \
		   -I$(DIR_IO) \
 		   $(CFLAGS_MPI) \
           $(CFLAGS_HDF5)

LDFLAGS = -fopenmp \
		  $(LFLAGS_MPI) \
          $(LFLAGS_HDF5)

ifneq ($(LIBDIR_MPI),)
LDFLAGS += -Wl,-rpath,$(LIBDIR_MPI)
endif

ifneq ($(LIBDIR_HDF5),)
LDFLAGS += -Wl,-rpath,$(LIBDIR_HDF5)
endif

# =======================================================
# LISTE DES FICHIERS SOURCE
# =======================================================

SRC_MAIN = main.cpp \
		   $(DIR_SRC)/solver.cpp \
		   $(wildcard $(DIR_SETUPS)/*.cpp) \
		   $(wildcard $(DIR_NUMERICS)/*.cpp) \
		   $(wildcard $(DIR_PHYSICS)/*.cpp) \
		   $(wildcard $(DIR_IO)/*.cpp)

SRC = $(SRC_MAIN)

# =======================================================
# LISTE DES FICHIERS OBJETS
# =======================================================

OBJ = $(SRC:%.cpp=$(DIR_OBJ)/%.o)

# =======================================================
# CIBLES UTILITAIRES
# =======================================================

.PHONY: all run clean

all: $(TARGET)

# =======================================================
# ÉDITION DE LIENS : FABRIQUER L’EXÉCUTABLE FINAL
# =======================================================

$(TARGET): $(OBJ)
	$(CXX) $(OBJ) $(LDFLAGS) $(LIBS_HDF5) $(LIBS_MPI) -o $@

# =======================================================
# RÈGLE DE COMPILATION : .cpp --> .o
# =======================================================

$(DIR_OBJ)/%.o: %.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -MMD -MP -c $< -o $@

# =======================================================
# CIBLE DE NETTOYAGE
# =======================================================

-include $(OBJ:.o=.d)

clean:
	rm -rf $(TARGET) $(DIR_OBJ)
