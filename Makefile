CXX=g++
CXXFLAGS=-std=c++17 -O2 -Wall

all: quantRush

quantRush: src/main.cpp
	$(CXX) $(CXXFLAGS) -o quantRush src/main.cpp

clean:
	rm -f quantRush
