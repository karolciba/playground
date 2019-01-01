#include <vector>
#include <array>
#include <iostream>
#include <set>
#include <SFML/Graphics.hpp>
#include <thread>
#include <future>


struct Point {
	unsigned char dot : 1;
	unsigned char west : 1;
	unsigned char south_west : 1;
	unsigned char south : 1;
	unsigned char south_east : 1;
    Point(): dot(0), west(0), south_west(0), south(0), south_east(0) {};
};

struct Coord {
	char x;
	char y;

	Coord(int ix, int iy) {
		x = static_cast<char>(ix);
		y = static_cast<char>(iy);
	}

	bool operator< (const Coord o) const {
		if (x < o.x) {
			return true;
		} else if (x == o.x) {
			return y < o.y;
		} else {
			return false;
		}
	}
};

/*
 *  0123456789ABCDEF
 * 0                0
 * 1                1
 * 2      ?  ?      2
 * 3     ?....?     3
 * 4      .  .      4
 * 5   ? ?.  .? ?   5
 * 6  ?....??....?  6
 * 7   .  ?  ?  .   7
 * 8   .  ?  ?  .   8
 * 9  ?....??....?  9
 * A   ? ?.  .? ?   A
 * B      .  .      B
 * C     ?....?     C
 * D      ?  ?      D
 * E                E
 * F                D
 *  0123456789ABCDEF
 */
struct Space {
    int depth = 0;
	std::array<std::array<Point,16>,16> space;
	std::set<Coord> options;

	Space() {
		space[3][6].dot = 1;
		space[3][7].dot = 1;
		space[3][8].dot = 1;
		space[3][9].dot = 1;
		space[4][6].dot = 1;
		space[4][9].dot = 1;
		space[5][6].dot = 1;
		space[5][9].dot = 1;
		space[6][3].dot = 1;
		space[6][4].dot = 1;
		space[6][5].dot = 1;
		space[6][6].dot = 1;
		space[6][9].dot = 1;
		space[6][10].dot = 1;
		space[6][11].dot = 1;
		space[6][12].dot = 1;

		space[7][3].dot = 1;
		space[7][12].dot = 1;
		space[8][3].dot = 1;
		space[8][12].dot = 1;
		space[9][3].dot = 1;
		space[9][4].dot = 1;
		space[9][5].dot = 1;
		space[9][6].dot = 1;
		space[9][9].dot = 1;
		space[9][10].dot = 1;
		space[9][11].dot = 1;
		space[9][12].dot = 1;
		space[10][6].dot = 1;
		space[10][9].dot = 1;
		space[11][6].dot = 1;
		space[11][9].dot = 1;
		space[12][6].dot = 1;
		space[12][7].dot = 1;
		space[12][8].dot = 1;
		space[12][9].dot = 1;

		options.insert({2,6});
		options.insert({2,9});
		options.insert({3,5});
		options.insert({3,10});
		options.insert({5,3});
		options.insert({5,5});
		options.insert({5,10});
		options.insert({5,12});
		options.insert({6,2});
		options.insert({6,7});
		options.insert({6,8});
		options.insert({6,13});
		options.insert({7,6});
		options.insert({7,9});
		options.insert({8,6});
		options.insert({8,9});
		options.insert({9,2});
		options.insert({9,7});
		options.insert({9,8});
		options.insert({9,13});
		options.insert({10,3});
		options.insert({10,5});
		options.insert({10,10});
		options.insert({10,12});
		options.insert({12,5});
		options.insert({12,10});
		options.insert({13,6});
		options.insert({13,9});
	}

	Space(const Space &s) {
        depth = s.depth;
		space = s.space;
		options = s.options;
	}

/*	Space(const Space &&s) {
		depth = s.depth;
		space = std::move(s.space);
		options = std::move(s.options);
	}*/

	bool is_west_line(Coord from) {
		int x = from.x;
		int y = from.y;

		if (x < 1 || y < 0 || x > 11 || y > 15) {
			return false;
		}

		return space[x-1][y].west != 1
			   && space[x][y].dot == 1
			   && space[x+1][y].dot == 1
			   && space[x+2][y].dot == 1
			   && space[x+3][y].dot == 1
			   && space[x+4][y].dot == 1
			   && space[x+4][y].west != 1;
	}

	void make_west_line(Coord from) {
		depth++;
		int x = from.x;
		int y = from.y;
		space[x][y].west = 1;
		space[x+1][y].west = 1;
		space[x+2][y].west = 1;
		space[x+3][y].west = 1;
	}

	bool is_south_west_line(Coord from) {
		int x = from.x;
		int y = from.y;
        if (x < 1 || y < 1 || x > 11 || y > 11) {
			return false;
		}

		return space[x-1][y-1].south_west != 1
			   && space[x][y].dot == 1
			   && space[x+1][y+1].dot == 1
			   && space[x+2][y+2].dot == 1
			   && space[x+3][y+3].dot == 1
			   && space[x+4][y+4].dot == 1
			   && space[x+4][y+4].south_west != 1;
	}

	void make_south_west_line(Coord from) {
		depth++;
		int x = from.x;
		int y = from.y;
		space[x][y].south_west = 1;
		space[x+1][y+1].south_west = 1;
		space[x+2][y+2].south_west = 1;
		space[x+3][y+3].south_west = 1;
	}

	bool is_south_line(Coord from) {
		int x = from.x;
		int y = from.y;

		if (x < 0 || y < 1 || x > 15 || y > 11) {
			return false;
		}

		return space[x][y-1].south != 1
			   && space[x][y].dot == 1
			   && space[x][y+1].dot == 1
			   && space[x][y+2].dot == 1
			   && space[x][y+3].dot == 1
			   && space[x][y+4].dot == 1
			   && space[x][y+4].south != 1;
	}

    void make_south_line(Coord from) {
		depth++;
		int x = from.x;
		int y = from.y;
		space[x][y].south = 1;
		space[x][y+1].south = 1;
		space[x][y+2].south = 1;
		space[x][y+3].south = 1;
	}

	bool is_south_east_line(Coord from) {
		int x = from.x;
		int y = from.y;

		if (x < 4 || y < 1 || x > 15 || y > 11) {
			return false;
		}

		return space[x+1][y-1].south_east != 1
			   && space[x][y].dot == 1
			   && space[x-1][y+1].dot == 1
			   && space[x-2][y+2].dot == 1
			   && space[x-3][y+3].dot == 1
			   && space[x-4][y+4].dot == 1
			   && space[x-4][y+4].south_east != 1;
	}

	void make_south_east_line(Coord from) {
		depth++;
		int x = from.x;
		int y = from.y;
		space[x][y].south_east = 1;
		space[x-1][y+1].south_east = 1;
		space[x-2][y+2].south_east = 1;
		space[x-3][y+3].south_east = 1;
	}

	void put_point(Coord point) {
		int x = point.x;
		int y = point.y;
		// put dot on options place
		space[x][y].dot = 1;
	}


	void extend_options(Coord point) {
		int x = point.x;
		int y = point.y;

        for (int xx=x-4; xx<=x+4; xx++) {
            if (xx < 0 || xx > 15) {
				continue;
			}
			for (int yy=y-4; yy<=y+4; yy++) {
				if (yy < 0 || yy > 15) {
					continue;
				}
                if (space[xx][yy].dot == 1) {
					continue;
				}

				options.insert({xx,yy});
			}
		}

	}

	void filter_options() {
        for (auto o : options) {
			auto cp {*this};
            cp.put_point(o);
            bool line = false;

			int x = o.x;
			int y = o.y;

            // make all south_west lines
            for (int xx = x-4, yy=y-4; xx <= x; xx++, yy++) {
                if (cp.is_south_west_line({xx, yy})) {
					line = true;
					break;
                }
            }
            if (line) {
				continue;
			}
            // make all south_east lines
            for (int xx = x+4, yy=y-4; yy <= y; xx--, yy++) {
                if (cp.is_south_east_line({xx, yy})) {
					line = true;
					break;
                }
            }
			if (line) {
				continue;
			}
            // make all west lines
            for (int xx = x-4; xx <= x; xx++) {
                if (cp.is_west_line({xx, y})) {
					line = true;
					break;
                }
            }
			if (line) {
				continue;
			}
            // make all south lines
            for (int yy = y-4; yy <= y; yy++) {
                if (cp.is_south_line({x, yy})) {
					line = true;
					break;
                }
            }
			if (line) {
				continue;
			} else {
				options.erase(o);
			}
		}
	}

	std::vector<Space> solve() {
        std::vector<Space> nexts;

		for (auto c : options) {
            auto copy { *this };
			auto ret = copy.solve(c);
            nexts.insert(nexts.end(),ret.begin(),ret.end());
		}

		return nexts;
	}

	std::vector<Space> solve(Coord place) {
		std::vector<Space> nexts;
		if (!options.size()) {
			return nexts;
		}
//		Coord place = *options.rbegin();
		options.erase(place);
		int x = place.x;
		int y = place.y;

		put_point(place);
        extend_options(place);

		// make all south_west lines
		for (int xx = x-4, yy=y-4; xx <= x; xx++, yy++) {
			if (is_south_west_line({xx, yy})) {
				Space next{*this};
				next.make_south_west_line({xx,yy});
				next.filter_options();
				nexts.push_back(next);
			}
		}
		// make all south_east lines
		for (int xx = x+4, yy=y-4; yy <= y; xx--, yy++) {
			if (is_south_east_line({xx, yy})) {
				Space next{*this};
				next.make_south_east_line({xx,yy});
				next.filter_options();
				nexts.push_back(next);
			}
		}
		// make all west lines
		for (int xx = x-4; xx <= x; xx++) {
			if (is_west_line({xx, y})) {
				Space next{*this};
				next.make_west_line({xx,y});
				next.filter_options();
				nexts.push_back(next);
			}
		}
		// make all south lines
		for (int yy = y-4; yy <= y; yy++) {
            if (is_south_line({x, yy})) {
                Space next{*this};
                next.make_south_line({x,yy});
				next.filter_options();
                nexts.push_back(next);
            }
        }

		return nexts;
	}

	friend std::ostream& operator <<(std::ostream& stream, const Space& sp);
};

std::ostream& operator <<(std::ostream& stream, const Space& sp) {
    stream << "Lines put: " << sp.depth;
	stream << " Options: " << sp.options.size();
//	stream << std::endl;
    stream << "\n";

    for (int x = 0; x < 16; x++) {
		for (int y = 0; y < 16; y++) {
                if (sp.space[x][y].west == 1
                        || sp.space[x][y].south_west == 1
                        || sp.space[x][y].south == 1
                        || sp.space[x][y].south_east == 1 ) {
					stream << "*";
				} else if (sp.space[x][y].dot == 1) {
					stream << ".";
				} else {
					stream << " ";
				}

		}
//		stream << std::endl;
        stream << "\n";
	}
	return stream;
}

struct Line {
	int x0;
	int y0;
	int x1;
	int y1;

	friend std::ostream& operator <<(std::ostream& stream, const Line& ln);
};

std::ostream& operator <<(std::ostream& stream, const Line& ln) {
    stream << "((";
	stream << static_cast<unsigned int>(ln.x0);
	stream << ",";
	stream << static_cast<int>(ln.y0);
    stream << "),(";
	stream << (int)ln.x1;
	stream << ",";
	stream << static_cast<unsigned int>(ln.y1);
	stream << "))";

	return stream;
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
					lines.push_back(Line {x,y,x-1,y+1});
				}
			}
		}
	}
};

int main() {
	sf::RenderWindow window(sf::VideoMode(600, 600), "SFML works!");

    Space sp;
    std::cout << sp;

	std::vector<Space> stack;
	stack.push_back(sp);

	int best_depth = 0;
	Space best_space = sp;

	while (stack.size() > 0) {
	    auto& el = *stack.rbegin();


        if (el.depth > best_depth) {
            best_depth = el.depth;
			Verbose vb{el};
			window.clear();
//			std::cout << el.depth << "\r" << " ";
            std::cout << el.depth << std::endl;
			for (auto ln : vb.lines) {
				sf::Vertex line[] =
						{
								sf::Vertex(sf::Vector2f(ln.x0 * 30, ln.y0 * 30)),
								sf::Vertex(sf::Vector2f(ln.x1 * 30, ln.y1 * 30))
						};

				window.draw(line, 2, sf::Lines);
			}
			window.display();
		}

        sf::Event event;
        while(window.pollEvent(event)) {}

//		std::cout << el << std::endl;
		auto nexts = el.solve();
		stack.pop_back();
		stack.insert(stack.end(),nexts.begin(),nexts.end());
	}
}
