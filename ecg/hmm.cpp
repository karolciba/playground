#include <valarray>

using namespace std;

class Model {
	public:
		int states;
		int symbols;
		valarray<float> initial;
		valarray<float> transitions;
		valarray<float> emissions;
		Model(int sta, int sym) : states {sta}, symbols {sym}, initial {valarray<float>(states)}, transitions {valarray<float>(states*states)}, emissions {valarray<float>(states*symbols)} {};

		void train(
	private:
};
