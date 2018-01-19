#include <vector>
#include <array>
#include <iostream>

struct Point {
	unsigned char dot : 1;
	unsigned char west : 1;
	unsigned char south_west : 1;
	unsigned char south : 1;
	unsigned char south_east : 1;
    Point(): dot(0), west(0), south_west(0), south(0), south_east(0) {};
};

struct Coord {
	unsigned char x;
	unsigned char y;
};

struct Space {
	std::array<std::array<Point,16>,16> space;
	std::vector<Coord> options;

	Space() {
		space[3][6].dot = 1;
		space[3][7].dot = 1;
		space[3][8].dot = 1;
		space[3][9].dot = 1;
	}

	Space(const Space &s) {
		space = s.space;
		options = s.options;
	}
};

struct Line {
	unsigned char x0;
	unsigned char y0;
	unsigned char x1;
	unsigned char y1;

	friend std::ostream& operator <<(std::ostream& stream, const Line& ln);
};

std::ostream& operator <<(std::ostream& stream, const Line& ln) {
	stream << static_cast<unsigned int>(ln.x0);
	stream << static_cast<int>(ln.y0);
	stream << (int)ln.x1;
	stream << static_cast<unsigned int>(ln.y1);
}

struct Verbose {
	std::vector<Line> lines;

	Verbose(Space space) {
		for (unsigned char x = 0; x < space.space.size(); x++) {
			auto& row = space.space[x];
			for (unsigned char y = 0; y < row.size(); y++) {
				auto &point = row[y];
				if (!point.dot) {
					continue;
				}

				lines.push_back(Line {x,y,x,y});
				if (point.west) {
					lines.push_back(Line {x,y,x+1,y});
				}
				if (point.south_west) {
					lines.push_back(Line {x,y,x+1,y+1});
				}
				if (point.south) {
					lines.push_back(Line {x,y,x,y+1});
				}
				if (point.south_east) {
					lines.push_back(Line {x,y,x-1,y-1});
				}
			}
		}
	}
};

int main() {

    Space sp;
    Verbose vb {sp};

//	std::cout << vb.lines;
    for (auto line : vb.lines) {
		std::cout << line << std::endl;
	}
}
