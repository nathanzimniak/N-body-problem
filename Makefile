# =======================================================
# CHOIX DU COMPILATEUR
# =======================================================

CXX = g++-15


# =======================================================
# ORGANISATION DES DOSSIERS
# =======================================================

SRC_DIR = src
OBJ_DIR = build
SETUPS_DIR = setups
NUMERICS_DIR = $(SRC_DIR)/numerics
PHYSICS_DIR = $(SRC_DIR)/physics
IO_DIR = $(SRC_DIR)/io


# =======================================================
# INFORMATIONS GÉNÉRALES SUR LA COMPILATION
# =======================================================

TARGET = main


# =======================================================
# DÉTECTION AUTOMATIQUE DES FLAGS HDF5
# =======================================================

HDF5_SHOW := $(shell h5c++ -show)

HDF5_CFLAGS := $(shell printf '%s\n' "$(HDF5_SHOW)" | tr ' ' '\n' | grep '^-I')

HDF5_LFLAGS := $(shell printf '%s\n' "$(HDF5_SHOW)" | tr ' ' '\n' | grep '^-L')

HDF5_LIBS := $(shell printf '%s\n' "$(HDF5_SHOW)" | tr ' ' '\n' | grep -E '^-l|^/.+\.(a|so|so\.[0-9.]+|dylib)$$')

HDF5_LIBDIR := $(shell printf '%s\n' "$(HDF5_SHOW)" | tr ' ' '\n' | grep '^-L' | head -n1 | sed 's/^-L//')


# =======================================================
# OPTIONS DE COMPILATION
# =======================================================

CXXFLAGS = -O3 \
           -std=c++20 \
           -fopenmp \
		   -I$(SRC_DIR) \
		   -I$(SETUPS_DIR) \
		   -I$(NUMERICS_DIR) \
		   -I$(PHYSICS_DIR) \
		   -I$(IO_DIR) \
           $(HDF5_CFLAGS)

LDFLAGS = -fopenmp \
          $(HDF5_LFLAGS)

ifneq ($(HDF5_LIBDIR),)
LDFLAGS += -Wl,-rpath,$(HDF5_LIBDIR)
endif


# =======================================================
# LISTE DES FICHIERS SOURCE
# =======================================================

SRC_MAIN = main.cpp \
		   $(SRC_DIR)/solver.cpp \
		   $(wildcard $(SETUPS_DIR)/*.cpp) \
		   $(wildcard $(NUMERICS_DIR)/*.cpp) \
		   $(wildcard $(PHYSICS_DIR)/*.cpp) \
		   $(wildcard $(IO_DIR)/*.cpp)

SRC = $(SRC_MAIN)


# =======================================================
# LISTE DES FICHIERS OBJETS
# =======================================================

OBJ = $(SRC:%.cpp=$(OBJ_DIR)/%.o)


# =======================================================
# CIBLES UTILITAIRES
# =======================================================

.PHONY: all run clean

all: $(TARGET)


# =======================================================
# ÉDITION DE LIENS : FABRIQUER L’EXÉCUTABLE FINAL
# =======================================================

$(TARGET): $(OBJ)
	$(CXX) $(OBJ) $(LDFLAGS) $(HDF5_LIBS) -o $@


# =======================================================
# RÈGLE DE COMPILATION : .cpp --> .o
# =======================================================

$(OBJ_DIR)/%.o: %.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -MMD -MP -c $< -o $@


# =======================================================
# CIBLE D’EXÉCUTION
# =======================================================

run: $(TARGET)
	./$(TARGET)


# =======================================================
# CIBLE DE NETTOYAGE
# =======================================================

-include $(OBJ:.o=.d)

clean:
	rm -rf $(TARGET) $(OBJ_DIR)